from django.forms import ModelForm, CharField, TextInput, ModelChoiceField
from .models import Quote, Tag, Author


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]


class QuoteForm(ModelForm):
    quote = CharField(min_length=5, max_length=800, required=True, widget=TextInput())
    # author = ModelChoiceField(queryset=Author.objects.all(), required=False)
    new_author = CharField(
        min_length=10, max_length=150, required=True, widget=TextInput()
    )

    class Meta:
        model = Quote
        fields = ["quote", "new_author"]
        exclude = ["tags"]


class AuthorForm(ModelForm):
    fullname = CharField(
        min_length=3, max_length=120, required=True, widget=TextInput()
    )

    class Meta:
        model = Author
        fields = ["fullname"]
