from django import forms

from .models import Post, User, Comment


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = (
            'author',
        )
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M',
                attrs={
                    'type': 'datetime-local'
                }
            )
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'text',
        )
