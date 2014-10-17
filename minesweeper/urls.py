from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'minesweeper.views.home', name='home'),
    # url(r'^minesweeper/', include('minesweeper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/(?P<name>(\w|\s)+)/(?P<game_id>\d+)/?$', 'game.views.game_start', name='game_start'),
    url(r'^game/(?P<name>(\w|\s)+)/(?P<game_id>\d+)/check/?$', 'game.views.game_check', name='game_check'),
    url(r'^$', 'game.views.index', name='index'),
)
