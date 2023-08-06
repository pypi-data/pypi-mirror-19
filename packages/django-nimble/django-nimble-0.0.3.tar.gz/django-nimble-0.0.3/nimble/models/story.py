from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from polymorphic.models import PolymorphicModel
from markdownx.models import MarkdownxField


class Story(PolymorphicModel):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = MarkdownxField(default='')

    def name(self):
        return '{}{:0>5}'.format(self.ident, self.id)

    def api_url(self):
        return reverse(self.api_detail_name, kwargs={
            'pk': self.pk,
        })

    @classmethod
    def api_keys(cls):
        return ['url', 'author', 'title', 'description']

    @classmethod
    def api_list_url(cls):
        return reverse(cls.api_list_name)
