from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostEditForm, ProfileEditForm, CommentEditForm
from .models import Post, Category, User, Comment
from django.utils import timezone


class IndexView(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = get_posts(Post.objects).order_by('-pub_date')

        context['page_obj'] = get_paginator(self.request, posts)
        return context


class PostDetailView(TemplateView):
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['id']

        post = get_object_or_404(
            Post,
            id=post_id
        )

        if self.request.user != post.author:
            post = get_object_or_404(get_posts(Post.objects), id=post_id)

        context['post'] = post
        context['form'] = CommentEditForm()
        context['comments'] = post.comments.order_by('created_at')

        return context


class CategoryPostsView(TemplateView):
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_slug = self.kwargs['category_slug']

        category = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True
        )

        posts = get_posts(category.posts).order_by('-pub_date')

        context['category'] = category
        context['page_obj'] = get_paginator(self.request, posts)

        return context


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostEditForm(
            request.POST or None,
            files=request.FILES or None
        )
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', request.user)
    else:
        form = PostEditForm()

    context = {
        'form': form
    }
    return render(request, 'blog/create.html', context)


def profile_detail(request, username):
    user = get_object_or_404(
        User,
        username=username
    )
    posts_list = (
        user.posts
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )

    page_obj = get_paginator(request, posts_list)

    context = {
        'profile': user,
        'page_obj': page_obj
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(
            request.POST,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('blog:profile', request.user)
    else:
        form = ProfileEditForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'blog/user.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id
    )

    if request.user != post.author:
        return redirect('blog:post_detail', post_id)

    if request.method == "POST":
        form = PostEditForm(
            request.POST,
            files=request.FILES or None,
            instance=post
        )
        if form.is_valid():
            post.save()
            return redirect('blog:post_detail', post_id)
    else:
        form = PostEditForm(instance=post)

    context = {
        'form': form
    }
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id
    )

    if request.user != post.author:
        return redirect('blog:post_detail', post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    else:
        form = PostEditForm(instance=post)

    context = {
        'form': form
    }
    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(
        Post, id=post_id
    )
    form = CommentEditForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

    return redirect('blog:post_detail', post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    if request.user != comment.author:
        return redirect('blog:post_detail', post_id)

    if request.method == "POST":
        form = CommentEditForm(
            request.POST or None,
            instance=comment
        )
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id)
    else:
        form = CommentEditForm(instance=comment)

    context = {
        'form': form,
        'comment': comment
    }
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    if request.user != comment.author:
        return redirect('blog:post_detail', post_id)

    if request.method == "POST":
        comment.delete()
        return redirect('blog:post_detail', post_id)

    context = {
        'comment': comment
    }
    return render(request, 'blog/comment.html', context)


def get_paginator(request, items, num=10):
    paginator = Paginator(items, num)
    num_pages = request.GET.get('page')
    return paginator.get_page(num_pages)


def get_posts(post_objects):
    return post_objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).annotate(comment_count=Count('comments'))
