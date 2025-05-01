from django.db import models
from custom_authentication.models import CustomUser
from core.models import BaseModel

# Create your models here.

class Bookshelf(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.name