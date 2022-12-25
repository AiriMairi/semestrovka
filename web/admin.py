from web.models import Course, User, UserInfo, Comment, Category
from django.contrib import admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'image']
    filter_horizontal = ['groups', 'user_permissions']
    fields = ['password', 'last_login', 'groups', ('username', 'email'), ('first_name', 'last_name'), 'image',
              ('is_active', 'is_staff')]
    ordering = ['-is_staff']


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'bio', 'avatar', 'is_teacher']
    fields = ['user', 'name', 'bio', 'avatar', 'is_teacher']
    ordering = ['is_teacher']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'tags', 'title', 'text', 'image', 'slug']
    fields = ['user', 'tags', 'title', 'text', 'image', 'slug', 'category']
    ordering = ['title']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['category']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'text', 'create_date']
    list_per_page = 5
    ordering = ['user']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_per_page = 5
    ordering = ['name']
