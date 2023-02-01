"""FreeLancer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.admin import *
from django.urls import path
from homePage.views import *
from CourseRecommendation.views import *

urlpatterns = [
    path('admin/', site.urls),
    path('',home),
    path("view_freelancers/", view_freelancers, name="view_freelancers"),
    path("view_hirers/", view_hirers, name="view_hirers"),
    #Freelancer
    path("freelancer_login/", freelancer_login, name="freelancer_login"),
    path("signup/", signup, name="signup"),
    path("freelancer_homepage/", freelancer_homepage, name="freelancer_homepage"),
    path("logout/", Logout, name="logout"),
    path("all_jobs/", all_jobs, name="all_jobs"),
    path("job_detail/<int:myid>/", job_detail, name="job_detail"),
    path("job_apply/<int:myid>/", job_apply, name="job_apply"),

    # Company
    path("company_signup/", company_signup, name="company_signup"),
    path("company_login/", company_login, name="company_login"),
    path("company_homepage/", company_homepage, name="company_homepage"),
    path("add_job/", add_job, name="add_job"),
    path("job_list/", job_list, name="job_list"),
    path("all_applicants/", all_applicants, name="all_applicants"),

    #Projects
    path("add_projects/", add_projects, name="add_projects"),
    path("view_projects/", view_projects, name="view_projects"),
    #path("filter_projects/<int:myid>/", filter_projects, name="filter_projects")

    #Course Recommendation
    path('courses/',course),
    path('courses/recommend_course/', recommend_course)
]
'''
    path('join/profile/',login_user),
    #path('portfolio/',port),
    path('join/',sign),
    path('join/portfolio/',signup_user),
    path('courses/',course),
    path('courses/recommend_course/', recommend_course),'''