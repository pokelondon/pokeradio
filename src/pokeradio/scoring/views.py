from django.conf import settings
from django.views.generic import ListView

from .models import Point, Credit


class StatementView(ListView):
    template_name = 'scoring/index.html'

    def get_queryset(self):
        return Point.objects.all()

point_statement = StatementView.as_view()
