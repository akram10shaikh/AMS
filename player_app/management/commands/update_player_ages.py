from django.core.management.base import BaseCommand
from player_app.models import Player
from player_app.utils import age_for_current_season

class Command(BaseCommand):
    help = "Recalculate Player.current_age based on season (September to September)"

    def handle(self, *args, **options):
        players = Player.objects.exclude(date_of_birth__isnull=True)
        to_update = []
        for p in players.iterator():
            new_age = age_for_current_season(p.date_of_birth)
            if p.current_age != new_age:
                p.current_age = new_age
                to_update.append(p)
        Player.objects.bulk_update(to_update, ["current_age"])
