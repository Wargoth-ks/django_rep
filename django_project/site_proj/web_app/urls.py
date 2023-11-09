from django.urls import path

from . import views

app_name = "web_app"

urlpatterns = [
    path("", views.main, name="main"),
    path("author/<str:name_author>/", views.author, name="author"),
    path("tag/<str:tag_name>/", views.quotes_by_tag, name="quotes_by_tag"),
    path("add_quote/", views.add_quote, name="add_quote"),
]
