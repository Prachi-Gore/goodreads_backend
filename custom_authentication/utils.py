from django.contrib.auth import get_user_model
from rest_framework import serializers

def get_user_by_email(email):
    """Fetch user by email, or raise a validation error if not found."""
    User = get_user_model()
    print('get_user_by_email list',User.objects.all())

    user = User.objects.filter(email=email).first()
    print('get_user_by_email ',user)
    if not user:
        raise serializers.ValidationError("No account found with this email.")
    return user