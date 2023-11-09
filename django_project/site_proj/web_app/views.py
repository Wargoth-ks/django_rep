from django.shortcuts import render, get_object_or_404, redirect
from web_app.models import Quote, Author, Tag
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import QuoteForm, AuthorForm


def main(request):
    quotes_list = Quote.objects.all().order_by("id")
    paginator = Paginator(quotes_list, 10)  # Show 10 quotes per page.
    page_number = request.GET.get("page", 1)
    quotes = paginator.get_page(page_number)
    quote_slices = [quotes[i : i + 2] for i in range(0, len(quotes), 2)]
    return render(
        request,
        "web_app/index.html",
        {"quote_slices": quote_slices, "page_obj": quotes},
    )


def author(request, name_author):
    author = get_object_or_404(Author, fullname=name_author)
    return render(request, "web_app/author.html", {"author": author})


def quotes_by_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    quotes = tag.quote_set.all()
    return render(
        request, "web_app/quotes_by_tag.html", {"quotes": quotes, "tag_name": tag_name}
    )


@login_required(login_url="/users/login/")
def add_quote(request):
    tags = Tag.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            # get the author from the form
            author_name = form.cleaned_data["new_author"]
            author = Author.objects.create(fullname=author_name)
            new_quote = form.save(commit=False)
            new_quote.author = author
            new_quote.quote = f"“{new_quote.quote}”"
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to="web_app:main")
        else:
            return render(
                request, "web_app/add_quote.html", {"tags": tags, "form": form}
            )

    return render(
        request, "web_app/add_quote.html", {"tags": tags, "form": QuoteForm()}
    )
