from django.test import TestCase

from django.test import TestCase
from .models import Category
from django.core.urlresolvers import reverse

# Перед заупском любого теста создаётся совершенно новая база данных, никак не связанная с
# с текущей базой приложения, и она асоцируется с добавлением любых сущеностей в тестах

class CategoryMethodTests(TestCase):

    # ensure_views_are_positive should results True for categories where views are zero or positive
    def test_ensure_views_are_positive(self):

        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    # slug_line_creation checks to make sure that when we add a category an appropriate slug line is created
    # i.e. "Random Category String" -> "random-category-string"
    def test_slug_line_creation(self):

        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


class IndexViewTests(TestCase):
    # Recall that when you run tests, a new database is created, which by default is not populated.

    # If no questions exist, an appropriate message should be displayed.
    def test_index_view_with_no_categories(self):

        response = self.client.get(reverse('index'))

        # check if the page loads
        self.assertEqual(response.status_code, 200)

        # the html contain the phrase “There are no categories present.”???
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])

    # If no questions exist, an appropriate message should be displayed.
    def test_index_view_with_categories(self):

        add_cat('test', 1, 1)
        add_cat('temp', 1, 1)
        add_cat('tmp', 1, 1)
        add_cat('tmp test temp', 1, 1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")

        self.assertNotContains(response, "There are no categories present.")

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


