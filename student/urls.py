from django.contrib.auth.views import LoginView
from django.urls import path

from student import views

urlpatterns = [
    path('studentclick', views.studentclick_view, name='student-click'),
    path('studentlogin', LoginView.as_view(
        template_name='student/studentlogin.html'), name='studentlogin'),
    path('studentsignup', views.student_signup_view, name='studentsignup'),
    path('student-dashboard', views.student_dashboard_view,
         name='student-dashboard'),
    path('student-check', views.student_check_view, name='student-check'),
    path('student-exam', views.student_exam_view, name='student-exam'),
    path('take-exam/<int:pk>', views.take_exam_view, name='take-exam'),
    path('start-exam/<int:pk>', views.start_exam_view, name='start-exam'),
    path('calculate-marks', views.calculate_marks_view, name='calculate-marks'),
    path('view-result', views.view_result_view, name='view-result'),
    path('check-marks/<int:pk>', views.check_marks_view, name='check-marks'),
    path('student-marks', views.student_marks_view, name='student-marks'),
    path('expel/<int:pk>', views.student_expel_view, name='expel'),
    path('video_feed', views.video_feed, name='video-feed'),
    path('train_feed', views.train_feed, name='train-feed'),
    path('check_feed', views.check_feed, name='check-feed'),
    path('logout', views.student_logout_view, name='student-logout'),
]
