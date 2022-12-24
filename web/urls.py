"""school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='main_page'),
    path('add_course', views.CourseCreateView.as_view(), name='course_create'),
    path('<slug:tag_slug>', views.TagIndexView.as_view(), name='courses_by_tag'),
    path("add-rating", views.AddStarRating.as_view(), name='add_rating'),
    path('<slug:slug>/<int:id>', views.CourseDetailView.as_view(), name='single_course'),
    path('<slug:slug>/<int:id>/delete', views.CourseDeleteView.as_view(), name='course_delete'),
    path('<slug:slug>/<int:id>/edit', views.CourseUpdateView.as_view(), name='course_update'),
    path('<slug:slug>/<int:course_id>/comment/<int:id>/delete', views.CommentDeleteView.as_view(),
         name='delete_comment'),
    path('<slug:slug>/<int:course_id>/comment/<int:id>/edit', views.CommentUpdateView.as_view(), name='update_comment'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout')
]
