from django.views.generic import View
from django.http import JsonResponse, Http404
from django.db.models import Q

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from students.models import Student


class StudentsView(View):

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def post(self, request, *args, **kwargs):
        course = request.POST.get('course', None)
        if course:
            students = Student.objects.filter(Q(courses__in=[course]), ~Q(dropped_out_from_course__in=[course])).all()
            data = [{'id': student.id, 'name': str(student)} for student in students]
            return JsonResponse(data, safe=False)
        raise Http404()



