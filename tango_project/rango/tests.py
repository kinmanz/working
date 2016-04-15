from django.test import TestCase

from django.test import TestCase
from .models import Category


class CategoryMethodTests(TestCase):

    # ensure_views_are_positive should results True for categories where views are zero or positive
    def test_ensure_views_are_positive(self):

        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)
        




