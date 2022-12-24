from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import UpdateView, DeleteView, CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from web.models import Course, Comment
from web.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, CommentForm, CourseForm


class TagIndexView(ListView):
    model = Course
    template_name = 'web/index.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.filter(tags__slug=self.kwargs.get('tag_slug'))

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            **super(TagIndexView, self).get_context_data(**kwargs),
            'most_popular_tags': Course.tags.most_common()[:3],
        }


class CourseListView(ListView):
    template_name = 'web/index.html'
    model = Course
    context_object_name = 'courses'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            **super(CourseListView, self).get_context_data(**kwargs),
            'most_popular_tags': Course.tags.most_common()[:3],
        }


class CourseCreateView(CreateView):
    template_name = 'web/add_course.html'
    form_class = CourseForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.title, allow_unicode=True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main_page')


# FormMixin - тк в DetailView нет form_class
class CourseDetailView(FormMixin, DetailView):
    template_name = 'web/course-single.html'
    form_class = CommentForm
    model = Course
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('single_post', args=(self.kwargs['slug'], self.kwargs['id']))


class CourseDeleteView(DeleteView):
    template_name = 'web/course_delete.html'
    model = Course
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('main_page')


class CourseUpdateView(UpdateView):
    template_name = 'web/course_edit.html'
    model = Course
    form_class = CourseForm
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title, allow_unicode=True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('single_post', args=(self.object.slug, self.object.id))


class CommentUpdateView(UpdateView):
    template_name = 'web/comment_edit.html'
    model = Comment
    form_class = CommentForm
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.text, allow_unicode=True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_game', args=(self.kwargs['slug'], self.kwargs['game_id']))

    def get_context_data(self, **kwargs):
        return {
            **super(CommentUpdateView, self).get_context_data(**kwargs),
            'slug': self.kwargs['slug'],
            'game_id': self.kwargs['game_id']
        }


class CommentDeleteView(DeleteView):
    model = Comment
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('detail_game', args=(self.kwargs['slug'], self.kwargs['game_id']))


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main_page'))
    else:
        form = UserLoginForm()
    return render(request, 'web/login.html', {
        'form': form
    })


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered')
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    return render(request, 'web/register.html', {
        'form': form
    })


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'web/profile.html', {
        'form': form,
    })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main_page'))
