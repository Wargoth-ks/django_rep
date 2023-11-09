from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = "Stop Postgres DB"

    def handle(self, *args, **options):
        result = subprocess.run(
            ["docker", "ps", "-q", "-f", "name=container"],
            capture_output=True,
            text=True,
        )

        if result.stdout.strip():
            print("\nPostgres DB is stopping!...\n")
            subprocess.run(["docker", "stop", "container"])
            print("\nDone!\n")
        else:
            print("\nPostgres DB was already stopped!\n")
