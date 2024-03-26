from django.contrib import admin
from django.urls import path
from student.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("signout/", logout_page, name="logout_page"),
    path("see_marks/<student_id>", see_marks, name="see_marks")
]
