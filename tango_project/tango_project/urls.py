"""tango_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, patterns, url
from django.conf import settings
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from django.shortcuts import redirect
from django.views.generic.base import RedirectView

# чтобы не откидывала на registartion complete page а на index
# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self, request):
        return '/rank/add_profile/'


urlpatterns = [
    url(r'^favicon1\.ico$', 'rango.views.my_image'),
    url(r'^favicon\.ico$', 'rango.views.my_image'),
    url(r'^admin/', admin.site.urls),
    # Examples:
    url(r'^$', 'rango.views.index', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #Add in this url pattern to override the default pattern in accounts.
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^rank/', include('rango.urls')),  # ADD THIS NEW TUPLE!
    url(r'^accounts/', include('registration.backends.simple.urls')),
]


# UNDERNEATH your urlpatterns definition, add the following two lines:
# if settings.DEBUG:
if True:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)','serve',{'document_root': settings.MEDIA_ROOT}), )