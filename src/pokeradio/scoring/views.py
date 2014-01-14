from django.conf import settings
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required

from .models import Point, Credit


class StatementView(ListView):
    """ Allows the current user to view their credits and history of
    transactions
    """
    template_name = 'scoring/user_statement.html'

    def get_queryset(self):
        return Credit.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        c = super(StatementView, self).get_context_data(**kwargs)
        c['my_credits'] = Credit.objects.total(user=self.request.user)
        return c

point_statement = login_required(StatementView.as_view())

index = login_required(
        TemplateView.as_view(template_name='scoring/index.html'))
