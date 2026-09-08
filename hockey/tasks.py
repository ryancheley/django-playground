import httpx2
from django.tasks import task

from hockey.models import Conference, Division, Season, Team, TeamSeason

SEASON_URL = (
    "https://lscluster.hockeytech.com/feed/index.php?feed=modulekit&view=seasons&key=ccb91f29d6744675&client_code=ahl"
)

SEASON_FIELDS = ("season_name", "shortname", "career", "playoff", "start_date", "end_date")
TEAM_FIELDS = ("team_code", "city", "nickname")


@task
def sync_team_season(user_id=None):
    seasons = Season.objects.all().order_by("season_id")

    created = updated = 0

    for season in seasons:
        TEAM_URL = f"https://lscluster.hockeytech.com/feed/index.php?feed=modulekit&view=statviewtype&stat=division&type=standings&season_id={season.pk}&key=ccb91f29d6744675&client_code=ahl"

        response = httpx2.get(TEAM_URL)
        response.raise_for_status()
        teams = response.json()["SiteKit"]["Statviewtype"]

        for team in teams:
            if team.get("team_id"):
                _, was_created = TeamSeason.objects.update_or_create(
                    division=Division.objects.get(division_id=team.get("division_id")),
                    team=Team.objects.get(team_id=team.get("team_id")),
                    season=Season.objects.get(pk=season.pk),
                    defaults={"modified_by_id": user_id},
                    create_defaults={"modified_by_id": user_id, "created_by_id": user_id},
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        message = f"There were {created} team/seasons created an {updated} team/seasons updated."
    return message


@task
def sync_conferences(user_id=None):
    seasons = Season.objects.all().order_by("season_id")

    created = updated = 0

    for season in seasons:
        TEAM_URL = f"https://lscluster.hockeytech.com/feed/index.php?feed=modulekit&view=statviewtype&stat=division&type=standings&season_id={season.pk}&key=ccb91f29d6744675&client_code=ahl"

        response = httpx2.get(TEAM_URL)
        response.raise_for_status()
        teams = response.json()["SiteKit"]["Statviewtype"]

        for team in teams:
            if team.get("team_id"):
                _, was_created = Conference.objects.update_or_create(
                    name=team.get("conference_name"),
                    defaults={"modified_by_id": user_id},
                    create_defaults={"modified_by_id": user_id, "created_by_id": user_id},
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        message = f"There were {created} conferences created an {updated} conferences updated."
    return message


@task
def sync_divisions(user_id=None):
    seasons = Season.objects.all().order_by("season_id")
    # seasons = Season.objects.filter(pk=18)

    created = updated = 0

    for season in seasons:
        TEAM_URL = f"https://lscluster.hockeytech.com/feed/index.php?feed=modulekit&view=statviewtype&stat=division&type=standings&season_id={season.pk}&key=ccb91f29d6744675&client_code=ahl"

        response = httpx2.get(TEAM_URL)
        response.raise_for_status()
        teams = response.json()["SiteKit"]["Statviewtype"]

        for team in teams:
            if team.get("team_id"):
                print(
                    season.pk,
                    team.get("divisname"),
                    Conference.objects.get(name=team.get("conference_name")),
                    Season.objects.get(pk=season.pk),
                )

                fields = {
                    "division_name": team.get("divisname"),
                    "conference_name": Conference.objects.get(name=team.get("conference_name")),
                    "season": Season.objects.get(pk=season.pk),
                }
                _, was_created = Division.objects.update_or_create(
                    division_id=team.get("division_id"),
                    defaults={**fields, "modified_by_id": user_id},
                    create_defaults={**fields, "modified_by_id": user_id, "created_by_id": user_id},
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        message = f"There were {created} conferences created an {updated} conferences updated."
    return message


@task
def sync_teams(user_id=None):

    seasons = Season.objects.all().order_by("season_id")

    for season in seasons:
        TEAM_URL = f"https://lscluster.hockeytech.com/feed/index.php?feed=modulekit&view=statviewtype&stat=division&type=standings&season_id={season.pk}&key=ccb91f29d6744675&client_code=ahl"

        response = httpx2.get(TEAM_URL)
        response.raise_for_status()
        teams = response.json()["SiteKit"]["Statviewtype"]

        created = updated = 0

        for team in teams:
            if team.get("team_id"):
                defaults = {k: team[k] for k in TEAM_FIELDS}
                defaults["active"] = False
                defaults["name"] = team.get("team_name")
                defaults["modified_by_id"] = user_id
                defaults["created_by_id"] = user_id

                _, was_created = Team.objects.update_or_create(
                    team_id=team["team_id"],
                    defaults=defaults,
                    create_defaults={
                        **defaults,
                    },
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        message = f"There were {created} teams created an {updated} teams updated."
    return message


@task
def sync_seasons(user_id=None):
    response = httpx2.get(SEASON_URL)
    response.raise_for_status()
    seasons = response.json()["SiteKit"]["Seasons"]

    created = updated = 0

    for season in seasons:
        defaults = {k: season[k] for k in SEASON_FIELDS}
        defaults["modified_by_id"] = user_id
        defaults["created_by_id"] = user_id

        _, was_created = Season.objects.update_or_create(
            season_id=season["season_id"],
            defaults=defaults,
            create_defaults={
                **defaults,
            },
        )
        if was_created:
            created += 1
        else:
            updated += 1
    message = f"There were {created} seasons created an {updated} seasons updated."
    return message


@task
def set_active_teams():
    current_season = Season.objects.get(active=True)
    active_teams = TeamSeason.objects.filter(season=current_season)
    for team in active_teams:
        team = Team.objects.get(pk=team.team_id)
        team.active = True
        team.save(update_fields=["active"])
    return "Active Teams have been set"
