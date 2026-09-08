from django.contrib import admin

from core.admin import BaseModelAdmin

from .models import Conference, Division, Season, Team, TeamSeason


@admin.register(TeamSeason)
class TeamSeasonAdmin(BaseModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(BaseModelAdmin):
    pass


@admin.register(Season)
class SeasonAdmin(BaseModelAdmin):
    pass


@admin.register(Conference)
class ConferenceAdmin(BaseModelAdmin):
    fields = [
        "id",
        "name",
        "created_by",
        "create_timestamp",
        "modified_by",
        "modify_timestamp",
    ]
    readonly_fields = (
        "id",
        "created_by",
        "create_timestamp",
        "modified_by",
        "modify_timestamp",
    )


@admin.register(Division)
class DivisionAdmin(BaseModelAdmin):
    pass
