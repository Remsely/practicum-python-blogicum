from django.contrib.auth.forms import UserCreationForm
from django.urls import path, include, reverse_lazy
from django.contrib import admin
from django.views.generic import CreateView

urlpatterns = [
    # static
    path(
        'pages/',
        include('pages.urls', namespace='pages')
    ),
    path(
        'admin/',
        admin.site.urls
    ),
    # auth
    path(
        'auth/',
        include('django.contrib.auth.urls')
    ),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
    # root
    path(
        '',
        include('blog.urls', namespace='blog')
    )
]

handler403 = 'pages.views.forbidden'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
