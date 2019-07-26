from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView, TemplateView
from lectures.views import AttendanceLectureView, LectureView, ApiListStudentsView, AttendanceLectureNotMe
from students.views import StudentsView
from teachers.views import TeachersView

api_urlpatterns = [
    path('students/', StudentsView.as_view()),
    path('teachers/', TeachersView.as_view()),
    path('lecture/<str:token>/students/', ApiListStudentsView.as_view())
]

urlpatterns = [
    path('', RedirectView.as_view(url='/admin')),
    path('welcome/<int:lecture_id>/', LectureView.as_view(), name='qr_page'),
    path('check/<str:token>/', AttendanceLectureView.as_view(), name='check'),
    path('check/<str:token>/notme', AttendanceLectureNotMe.as_view(), name='notme'),
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
]

admin.site.site_header = 'Courses Manager'

handler404 = TemplateView.as_view(template_name='404.html')
