from django.urls import path
from neapolitan.views import Role

from hockey.views import ConferenceView, DivisionView, SeasonView, TeamSeasonView, TeamView, get_data, load_data

urlpatterns = [
    path("", load_data, name="load-data"),
    path("get-data/", get_data, name="get-data"),
    *SeasonView.get_urls(roles={Role.LIST, Role.DETAIL, Role.UPDATE}),
    *TeamView.get_urls(roles={Role.LIST, Role.DETAIL}),
    *TeamSeasonView.get_urls(roles={Role.LIST, Role.DETAIL}),
    *ConferenceView.get_urls(roles={Role.LIST, Role.DETAIL}),
    *DivisionView.get_urls(roles={Role.LIST, Role.DETAIL}),
]
