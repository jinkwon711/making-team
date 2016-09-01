"""tobusan URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from category import views as category_views
from accounts import views as account_views
from registration.backends.default.views import ActivationView, RegistrationView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', category_views.index, name='index'),
    url(r'^post_new/$', category_views.post_new, name='post_new'),
    url(r'^base/$', category_views.base),
    url(r'^search/$', category_views.main_search, name='main_search'),
    url(r'^category/(?P<tag>\w+)/$', category_views.select_search, name='select_search'),
    url(r'^post/(?P<pk>\d+)/$', category_views.post_detail),
     url(r'^post/(?P<post_pk>\d+)/comment_del/(?P<pk>\d+)', category_views.comment_delete),
    url(r'^post/(?P<pk>\d+)/edit/', category_views.post_edit),
    url(r'^post/(?P<pk>\d+)/del', category_views.post_delete),
    url(r'^post_apply/(?P<pk>\d+)/$', category_views.post_apply, name= 'post_apply'),

    url(r'^apply_delete/(?P<pk>\d+)/$', category_views.apply_delete,),
    url(r'^post/(?P<post_pk>\d+)/apply_delete_admin/(?P<user_pk>\d+)/$', category_views.apply_delete_admin),

    url(r'^mypage/$', category_views.mypage),
    url(r'^mypage/edit/$',account_views.profile_edit),

    url(r'^category/(?P<pk>\w+)/$',category_views.post_list),

    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(),
        name='registration_activate'),

]
# why?
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
