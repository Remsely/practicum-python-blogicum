from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from .models import Post, Category
from django.utils import timezone
from django.conf import settings


class IndexView(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post_list'] = Post.objects.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ).order_by('-pub_date')[:settings.POSTS_PER_PAGE]

        return context


class PostDetailView(TemplateView):
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['id']
        print(post_id)

        post = get_object_or_404(
            Post,
            id=post_id,
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )

        context['post'] = post

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

        context['category'] = category

        context['post_list'] = Post.objects.filter(
            category=category,
            is_published=True,
            pub_date__lte=timezone.now()
        )
        return context
