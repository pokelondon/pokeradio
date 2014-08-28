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

    # Points
    url(r'^fake-internet-points/$', 'points_index', name='points_index'),
    url(r'^fake-internet-points/(?P<year>\d{4})/(?P<week>\d+)/$', 'points_week',
        name='points_week'),

    # Leaderboard
    url(r'^playas/$', TemplateView.as_view(template_name='coming_soon.html'),
        name='leaderboard_index'),
    #url(r'^playas/$', 'leaderboard_index', name='leaderboard_index'),
    #url(r'^playas/(?P<year>\d{4})/(?P<week>\d+)/$', 'leaderboard',
        #name='leaderboard'),

    # Graphs
    url(r'^graph/force/$',
        TemplateView.as_view(template_name="scoring/graph_force.html"),
        name='graph_force'),
    url(r'^graph/wheel/$',
        TemplateView.as_view(template_name="scoring/graph_wheel.html"),
        name='graph_wheel'),

    # JSON data for graphs
    url(r'^force.json$', 'force_graph_json', name='force_graph_json'),
    url(r'^wheel.json$', 'wheel_graph_json', name='wheel_graph_json'),
]
urlpatterns += patterns('pokeradio.scoring.views', *urls)
