from django.core.management.base import BaseCommand
from web_app.models import Author
from web_app.models import Quote
from web_app.models import Tag
from tqdm import tqdm

import pymongo
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")


class Command(BaseCommand):
    help = "Migrate MongoDB to Postgres"

    def handle(self, *args, **options):
        try:
            mongo_client = pymongo.MongoClient(
                f"mongodb+srv://{env('MONGO_DB_USER')}:{env('MONGO_DB_PASSWORD')}@{env('MODGO_DB_DOMAIN')}/"
            )
            mongo_db = mongo_client[f"{env('MONGO_DB_NAME')}"]
            mongo_authors = mongo_db["author"]
            mongo_quotes = mongo_db["quote"]

            author_progress = tqdm(
                mongo_authors.find(), total=mongo_authors.count_documents({})
            )

            for doc in author_progress:
                postgres_author = Author(
                    fullname=doc["fullname"],
                    born_date=doc["born_date"],
                    born_location=doc["born_location"],
                    description=doc["description"],
                )
                postgres_author.save()

                author_progress.set_description(
                    f"\nAuthors migration: {doc['fullname']}"
                )

            quote_progress = tqdm(
                mongo_quotes.find(), total=mongo_quotes.count_documents({})
            )

            for doc in quote_progress:
                postgres_quote = Quote(quote=doc["quote"])
                postgres_quote.author_id = Author.objects.get(
                    fullname=mongo_authors.find_one({"_id": doc["author"]})["fullname"]
                ).id
                postgres_quote.save()
                for tag in doc["tags"]:
                    tag_obj, created = Tag.objects.get_or_create(name=tag)
                    postgres_quote.tags.add(tag_obj)

                quote_progress.set_description(
                    f"\nQuotes migration: {doc['quote'][:20]}..."
                )

            mongo_client.close()
            print("\nMigration to the Postgres DB is successful!\n")
        except Exception as e:
            print(e)
