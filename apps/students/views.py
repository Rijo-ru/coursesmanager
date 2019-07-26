from django.views.generic import View
from django.http import JsonResponse, Http404

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
        if request.POST['course']:
            students = Student.objects.filter(courses__in=[request.POST['course']]).all()
            data = [{'id': student.id, 'name': str(student)} for student in students]
            return JsonResponse(data, safe=False)
        raise Http404()



