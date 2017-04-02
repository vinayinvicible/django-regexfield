from django.db import models
from django.utils.six import python_2_unicode_compatible

from regexfield.fields import RegexField


@python_2_unicode_compatible
class Page(models.Model):
    url = RegexField('url path')

    def __str__(self):
        return self.url
