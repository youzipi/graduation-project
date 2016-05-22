from django.db.models import Model, Field, CharField


class User(Model):
    class Meta:
        name = CharField(max_length=20, )
