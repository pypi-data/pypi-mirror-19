from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.urlresolvers import reverse_lazy

from django.shortcuts import get_object_or_404

from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import FormView
from django.views.generic import ListView

from .models import Domain, Mailbox, UserProfile
from .forms import UserProfileAuthenticationForm


class IndexView(TemplateView):

    template_name = 'maccman/index.html'


class LoginView(FormView):

    template_name = 'maccman/login.html'
    form_class = UserProfileAuthenticationForm
    index = reverse_lazy('maccman:index')

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.index)
        return context

    def get_success_url(self):
        return self.request.POST.get('next', self.index)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):

    permanent = False
    query_string = False
    pattern_name = 'maccman:index'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class UserDomainsListView(LoginRequiredMixin, ListView):

    template_name = 'maccman/user_domain_list.html'
    model = Domain
    context_object_name = 'allowed_domains'
    login_url = reverse_lazy('maccman:login')

    def get_queryset(self):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        if profile:
            return profile.domain_set.all().order_by('name')
        return []

    def get_context_data(self, **kwargs):
        context = super(UserDomainsListView, self).get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        if profile:
            owned = profile.allowed_domains.all().order_by('name')
            context['owned_domains'] = owned
        return context


class UserMailboxesListView(LoginRequiredMixin, ListView):

    template_name = 'maccman/user_mailbox_list.html'
    model = Mailbox
    context_object_name = 'mailboxes'
    login_url = reverse_lazy('maccman:login')

    def get_queryset(self):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        return profile.mailbox_set.all().order_by('domain__name', 'account')
