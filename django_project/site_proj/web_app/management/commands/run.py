from django.core.management.base import BaseCommand
import subprocess
import time
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")


class Command(BaseCommand):
    help = "Run postgres database in docker with django server"

    def handle(self, *args, **options):
        try:
            print("Checking if postgresql << post_db >> is running...")

            result = subprocess.run(
                ["docker", "ps", "-q", "-f", "name=container"],
                capture_output=True,
                text=True,
            )

            if result.stdout.strip():
                print("\nPostgres DB is already running!")
            else:
                print("\nStarting postgresql << post_db >> ...\n")

                subprocess.run(
                    [
                        "docker",
                        "run",
                        "--rm",
                        "-d",
                        "--name",
                        "container",
                        "-p",
                        f"{env('DATABASE_PORT')}:{env('DATABASE_PORT')}",
                        "-e",
                        f"POSTGRES_PASSWORD={env('DATABASE_PASSWORD')}",
                        "-e",
                        f"POSTGRES_USER={env('DATABASE_USER')}",
                        "-e",
                        f"POSTGRES_DB={env('DATABASE_NAME')}",
                        "postgres:alpine",
                    ]
                )

                time.sleep(10)
                print("\nPostgres DB is running!")

            print("\nStarting Django server...")
            print("\nRun Django server + PostgresDB --> python manage.py run")
            print(
                "\nMigration from MongoDB to the PostgresDB --> python manage.py get_mongo_db"
            )
            print("\nStop PostgresDB --> python manage.py stop_db\n")
            subprocess.run(["python", "manage.py", "runserver"])
        except KeyboardInterrupt:
            print("\nServer is down\n")
