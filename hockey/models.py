from django.db import models

from core.models import Base


class Team(Base):
    team_id = models.IntegerField(primary_key=True)
    team_code = models.CharField(max_length=5)
    active = models.BooleanField()
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    nickname = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.city} {self.name} ({self.team_id})"


class Season(Base):
    season_id = models.IntegerField(primary_key=True)
    season_name = models.CharField(max_length=120)
    shortname = models.CharField(max_length=120)
    career = models.BooleanField()
    playoff = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.season_name} ({self.season_id})"


class Conference(Base):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Division(Base):
    division_id = models.IntegerField(primary_key=True)
    division_name = models.CharField(max_length=120)
    conference_name = models.ForeignKey(Conference, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return self.division_name


class TeamSeason(Base):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        display = f"{self.team.name} - {self.season.season_name}"  # ty: ignore[unresolved-attribute]
        return display
