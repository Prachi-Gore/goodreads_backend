from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import requests

from .models import Book

@receiver(post_save, sender=Book)
def add_book_summary_fastapi(sender, instance, created, **kwargs):
    print('serialize_book.data before',instance)
    if created:
        # Send book data to FastAPI AI endpoint
        print('serialize_book.data ',instance)
        print(instance.id)          # a234
        print(instance.title)       # King Salim
        print(instance.author.id)   # 214b3fb8-95ae-4cdd-a8b0-8c464c955dfe
        print(instance.author.author_name)  # Suraj Wagh
        data = {
            "id": str(instance.id),
            "title": instance.title,
            "author": str(instance.author.author_name)
        }
        try:
            requests.post(f"{settings.FASTAPI_URL}/add_book_summary", json=data)
        except Exception as e:
            print("Failed to generate book summary:", e)
