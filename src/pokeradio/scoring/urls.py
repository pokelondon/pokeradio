"""
.. module:: pokeradio.scoring.urls
   :synopsis: URLs for the scoring app
"""

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('')

urls = [
    url(r'^$', 'index', name='index'),

    # Credits
    url(r'^disco-biscuits/$', 'credits_index', name='credits_index'),
    url(r'^disco-biscuits/(?P<year>\d{4})/(?P<week>\d+)/$', 'credits_week',
        name='credits_week'),

    # Points
    url(r'^fake-internet-points/$', 'points_index', name='points_index'),
    url(r'^fake-internet-points/(?P<year>\d{4})/(?P<week>\d+)/$', 'points_week',
        name='points_week'),
    # JSON
    url(r'^graph/force/$',
        TemplateView.as_view(template_name="scoring/graph_force.html"),
        name='graph_force'),
    url(r'^graph/wheel/$',
        TemplateView.as_view(template_name="scoring/graph_wheel.html"),
        name='graph_wheel'),
    url(r'^force.json$', 'force_graph_json', name='force_graph_json'),
    url(r'^wheel.json$', 'wheel_graph_json', name='wheel_graph_json'),
]
urlpatterns += patterns('pokeradio.scoring.views', *urls)
