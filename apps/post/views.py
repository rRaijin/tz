from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostCreateForm
from .models import Post


class UserList(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'user/user-list.html'
    paginate_by = 4


class UserDetail(DetailView):
    model = User
    template_name = 'user/user-detail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.object).order_by('-created_date')
        return context


class PostsList(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post/post-list.html'
    paginate_by = 4

    def get_queryset(self, queryset=None):
        if not queryset:
            queryset = Post.objects.filter(is_published=True).order_by('-updated_date')
        return queryset


class PostDetail(DetailView):
    model = Post
    template_name = 'post/post-detail.html'
    pk_url_kwarg = 'id'


class PostCreate(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'post/post-create.html'
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().post(request, *args, **kwargs)
        else:
            raise Http404

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return redirect('post:detail', id=self.object.id)

    def get_success_url(self):
        return redirect('post:detail', id=self.kwargs['id'])


class PostUpdate(UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'post/post-create.html'
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        obj = Post.objects.get(id=self.kwargs['id'])
        if request.user == obj.author or request.user.is_staff:
            return super().get(request, *args, **kwargs)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        obj = Post.objects.get(id=self.kwargs['id'])
        if request.user == obj.author or request.user.is_staff:
            return super().post(request, *args, **kwargs)
        else:
            raise Http404

    def get_success_url(self):
        return reverse('post:detail', kwargs={'id':self.object.id})


class PostDelete(DeleteView):
    model = Post
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user == self.object.author or request.user.is_staff:
            self.object.delete()
            return redirect('post:list')
        else:
            raise Http404
