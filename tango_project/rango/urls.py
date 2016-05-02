from django.conf.urls import patterns, url
from django.conf import settings
from . import views

# app_name = 'rango'
# излишне для меня потому что у меня спецификация rango в url если бы её не было то пришлось бы

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.index_about, name='index_about'),
        url(r'^new/$', views.index2, name='index2'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        url(r'^change_category/$', views.change_category, name='change_category'),
        url(r'^change_page/$', views.change_page, name='change_page'),

        # слово + дефис + любое их количество до слеша /
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),

        # url(r'^register/$', views.register, name='register'),
        # url(r'^login/$', views.user_login, name='login'),
        url(r'^restricted/', views.restricted, name='restricted'),
        url(r'^search/', views.search, name='search'),
        # url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^example/$', views.some_view, name='some_view'),
        url(r'^like_category/$', views.like_category, name='like_category'),
        url(r'^add_profile/$', views.register_profile, name='add_profile'),
        url(r'^profile/(?P<user_name>[\w\-]+)/$', views.profile, name='profile'),
        url(r'^lockid/(?P<lockid>[\w\-]+)/$', views.lockid, name='lockid'),
        url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
        url(r'^auto_add_page/$', views.auto_add_page, name='auto_add_page'),
        url(r'^lock/$', views.lock, name='lock'),
        url(r'^goto/$', views.track_url, name='goto'),
        url(r'^restricted/$', views.restricted, name='restricted'),
]

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     # Examples:
#     # url(r'^$', 'tango_with_django_project_17.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#     url(r'^rango/', include('rango.urls')),  # ADD THIS NEW TUPLE!
# ]


