from django.conf.urls import url
from django.core.urlresolvers import reverse

from . import views

app_name = 'maccman'

urlpatterns = [
    url(r'^$',
        views.IndexView.as_view(),
        name='index',),

    url(r'^login$',
        views.LoginView.as_view(),
        name='login',),

    url(r'^logout$',
        views.LogoutView.as_view(),
        name='logout',),

    url(r'^domains$',
        views.UserDomainsListView.as_view(),
        name='domains',),

    url(r'^mailboxes$',
        views.UserMailboxesListView.as_view(),
        name='mailboxes',),
]
