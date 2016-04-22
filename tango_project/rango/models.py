from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()
    date_of_creation = models.DateField(default=timezone.now())
    author = models.ForeignKey(User)
    information = models.CharField(max_length=1000, default="No information present.")

    def save(self, *args, **kwargs):
            # Uncomment if you don't want the slug to change every time the name changes
            #if self.id is None:
                    #self.slug = slugify(self.name)
            self.slug = slugify(self.name)

            if not self.id:
                self.date_of_creation = timezone.now()

            if self.views < 0 or self.likes < 0:
                self.views = self.likes = 0
            super(Category, self).save(*args, **kwargs)

    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    last_visit = models.DateTimeField(default=timezone.now())
    information = models.CharField(max_length=200, default="")


    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        return super(Page, self).save(*args, **kwargs)

    def __str__(self):      #For Python 2, use __str__ on Python 3
        return self.title


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    # blank = True то есть заполнение по желанию, они могут быть пусты
    website = models.URLField(blank=True)
    # in all profile images being stored in the directory
    #  <workspace>/tango_with_django_project/media/profile_images/.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username