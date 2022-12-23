from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import UpdateView, DeleteView, CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin

from models import Course, Comment


class CourseListView(ListView):
    template_name = 'website/main_page.html'
    model = Course
    context_object_name = 'posts'
    slug_field = 'id'
    slug_url_kwarg = 'id'


class CourseCreateView(CreateView):
    template_name = 'website/post_add.html'
    form_class = CourseForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.title, allow_unicode=True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main_page')


# FormMixin - тк в DetailView нет form_class
class CourseDetailView(FormMixin, DetailView):
    template_name = 'website/single.html'
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
    template_name = 'website/post_delete.html'
    model = Post
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('main_page')


class CourseUpdateView(UpdateView):
    template_name = 'website/post_edit.html'
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
