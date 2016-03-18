from django.conf.urls import patterns, url
from django.conf import settings
from . import views

# app_name = 'rango'
# излишне для меня потому что у меня спецификация rango в url если бы её не было то пришлось бы

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.index_about, name='index_about'),
        url(r'^new/$', views.index2, name='index2'),
        # слово + дефис + любое их количество до слеша /
        url(r'^add_category/$', views.add_category, name='add_category'), # NEW MAPPING!
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category')]

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     # Examples:
#     # url(r'^$', 'tango_with_django_project_17.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#     url(r'^rango/', include('rango.urls')),  # ADD THIS NEW TUPLE!
# ]


