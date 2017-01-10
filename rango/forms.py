# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from rango.models import Page, Category, UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # data insert into model (before invoke clead() method) and invoke method save()
    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    # только модифицируем поля, не создаем!
    title = forms.CharField(max_length=128, help_text="Please enter page's title")
    url = forms.URLField(max_length=200, help_text="Please enter the URL")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    # This method is called before saving form data to a new model instance
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            return cleaned_data
