import re

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.db.models import Q
from django.views.generic import View
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from lectures.models import Lecture, AttendanceLecture
from students.models import Student


class AttendanceLectureView(View):
    template = 'student_check.html'
    template_cookie = 'student_check_identity.html'

    def get(self, request, token, *args, **kwargs):
        try:
            lecture = Lecture.objects.get(link_token=token)
        except Lecture.DoesNotExist:
            raise Http404()
        context = dict()
        context['link_token'] = token
        context['lecture_name'] = lecture.name
        identity = request.COOKIES.get('identity', None)
        if identity:
            try:
                student = lecture.register_students.get(
                        Q(identity_token=identity),
                        ~Q(dropped_out_from_lectures__in=[lecture])
                    )
            except Student.DoesNotExist:
                raise Http404()
            else:
                context['username'] = student.incognito_name
                attendance_lecture, created = AttendanceLecture.objects.get_or_create(lecture=lecture, student=student)
                if created:
                    layer = get_channel_layer()
                    async_to_sync(layer.group_send)(
                        lecture.link_token,
                        {
                            'type': 'lecture_notification',
                            'message': {'student_id': student.id, 'status': 'approved'}
                        }
                    )
                return render(request, self.template_cookie, context)
        return render(request, self.template, context)

    @method_decorator(csrf_protect)
    def post(self, request, token, *args, **kwargs):
        try:
            lecture = Lecture.objects.get(link_token=token)
        except Lecture.DoesNotExist:
            raise Http404()
        phone = request.POST.get('phone_number', None)
        student_id = request.POST.get('student_id', None)
        if phone:
            if re.match(r'^\d{10}$', phone):
                try:
                    student = lecture.register_students.get(
                        Q(phone_number=phone),
                        ~Q(dropped_out_from_lectures__in=[lecture])
                    )
                except Student.DoesNotExist:
                    return JsonResponse(status=400, data={'error': 'Неверный номер телефона!'})
                attendance_lecture, created = AttendanceLecture.objects.get_or_create(lecture=lecture, student=student)
                if created:
                    response = HttpResponse()
                    response.set_cookie('identity', student.identity_token)
                    return response
                else:
                    return JsonResponse(status=400, data={'error': 'Пользователь уже отмечен!'})
            else:
                return JsonResponse(status=400, data={'error': 'Неверный номер телефона!'})
        elif student_id:
            if re.match(r'^\d+$', student_id):
                try:
                    # student = Student.objects.get(id=student_id)
                    student = lecture.register_students.get(
                        Q(id=student_id),
                        ~Q(dropped_out_from_lectures__in=[lecture])
                    )
                except Student.DoesNotExist:
                    return JsonResponse(status=400, data={'error': 'Пользователь не найден!'})
                attendance_lecture, created = AttendanceLecture.objects.get_or_create(lecture=lecture, student=student)
                if created:
                    response = HttpResponse()
                    response.set_cookie('identity', student.identity_token)
                    layer = get_channel_layer()
                    async_to_sync(layer.group_send)(
                        lecture.link_token,
                        {
                            'type': 'lecture_notification',
                            'message': {'student_id': student.id, 'status': 'approved'}
                        }
                    )
                    return response
                else:
                    return JsonResponse(status=400, data={'error': 'Пользователь уже отмечен!'})
            else:
                return JsonResponse(status=400, data={'error': 'Пользователь не найден!'})
        else:
            return JsonResponse(status=400, data={'error': 'Данные не были получены.'})


class AttendanceLectureNotMe(View):

    @method_decorator(csrf_protect)
    def post(self, request, token, *args, **kwargs):
        try:
            lecture = Lecture.objects.get(link_token=token)
        except Lecture.DoesNotExist:
            raise Http404()
        identity = request.COOKIES.get('identity', None)
        if identity:
            try:
                student = lecture.register_students.get(
                        Q(identity_token=identity),
                        ~Q(dropped_out_from_lectures__in=[lecture])
                    )
            except Student.DoesNotExist:
                raise Http404()
            else:
                AttendanceLecture.objects.filter(lecture=lecture, student=student).delete()
                layer = get_channel_layer()
                async_to_sync(layer.group_send)(
                    lecture.link_token,
                    {
                        'type': 'lecture_notification',
                        'message': {'student_id': student.id, 'status': 'unapproved'}
                    }
                )
                response = redirect('check', token=token)
                response.delete_cookie('identity')
                return response
        else:
            return redirect('check', token=token)


class LectureView(View):
    template = 'qr_index.html'

    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def get(self, request, lecture_id, *args, **kwargs):
        try:
            lecture = Lecture.objects.prefetch_related('register_students', 'marked_students').get(id=lecture_id)
        except Lecture.DoesNotExist:
            raise Http404()
        context = dict()
        context['lecture_name'] = lecture.name
        context['token'] = lecture.link_token
        query_students = lecture.register_students.filter(~Q(dropped_out_from_lectures__in=[lecture]))
        context['students'] = query_students.all()
        context['count_students'] = query_students.count()
        query_marked_students = lecture.marked_students
        context['marked_students'] = [attended_lecture.student for attended_lecture in query_marked_students.select_related('student').all()]
        context['count_marked_students'] = query_marked_students.count()

        return render(request, self.template, context)


class ApiListStudentsView(View):

    items_on_page = 10

    @method_decorator(csrf_protect)
    def post(self, request, token, *args, **kwargs):
        try:
            lecture = Lecture.objects.prefetch_related('register_students').get(link_token=token)
        except Lecture.DoesNotExist:
            return HttpResponse(status=400)
        search = request.POST.get('search', "")
        page = 1
        if request.POST.get('page', '1').isdigit():
            page = int(request.POST.get('page', '1'))
        query_students = lecture.register_students.filter(
            Q(full_name__icontains=search),
            ~Q(dropped_out_from_lectures__in=[lecture])
        )
        data = dict()
        data['items'] = [{student.id: student.full_name}
                         for student in query_students.all()[(page-1)*self.items_on_page:page*self.items_on_page]]
        data['pagination'] = {'more': page*self.items_on_page < query_students.count()}
        return JsonResponse(status=200, data=data, safe=False)

