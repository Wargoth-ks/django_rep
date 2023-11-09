from django.db import models


# Create your models here.
#
class Author(models.Model):
    fullname = models.CharField(max_length=120)
    born_date = models.CharField(max_length=20)
    born_location = models.CharField(max_length=120)
    description = models.CharField()

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    quote = models.CharField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quote}"
