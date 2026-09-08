from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from neapolitan.views import CRUDView

from .models import Conference, Division, Season, Team, TeamSeason
from .tasks import set_active_teams, sync_conferences, sync_divisions, sync_seasons, sync_team_season, sync_teams


def load_data(request):
    return render(request, template_name="hockey/load_data.html", context={"title": "Data"})


@login_required
@require_POST
def get_data(request):
    result_seasons = sync_seasons.enqueue(user_id=request.user.pk)
    request.session["season_sync_id"] = result_seasons.id

    result_conferences = sync_conferences.enqueue(user_id=request.user.pk)
    request.session["season_sync_id"] = result_conferences.id

    result_divisions = sync_divisions.enqueue(user_id=request.user.pk)
    request.session["season_sync_id"] = result_divisions.id

    result_teams = sync_teams.enqueue(user_id=request.user.pk)
    request.session["team_sync_id"] = result_teams.id

    results_active_team = set_active_teams.enqueue()
    request.session["active_team_id"] = results_active_team.id

    result_team_season = sync_team_season.enqueue(user_id=request.user.pk)
    request.session["team_sync_id"] = result_team_season.id

    messages.info(request, "Sync started")
    return redirect("load-data")


class SeasonView(LoginRequiredMixin, CRUDView):
    model = Season
    fields = ["season_name", "shortname", "career", "playoff", "start_date", "end_date"]


class TeamView(LoginRequiredMixin, CRUDView):
    model = Team
    fields = ["team_code", "active", "name", "city", "nickname"]


class ConferenceView(LoginRequiredMixin, CRUDView):
    model = Conference
    fields = ["name"]


class DivisionView(LoginRequiredMixin, CRUDView):
    model = Division
    fields = ["division_name", "conference_name", "season"]


class TeamSeasonView(LoginRequiredMixin, CRUDView):
    model = TeamSeason
    fields = ["division", "team", "season"]
