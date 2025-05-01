from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel

# Create your models here.
User=get_user_model()

class ConnectionRequest(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    sender=models.ForeignKey(User,related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sender', 'receiver'], name='unique_connection_request')
        ]

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"
    

class Notification(BaseModel):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications') # notification receiver
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"To: {self.recipient.username} | {self.message}"

class Group(BaseModel):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='created_groups', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='groups_for_user')
    admins = models.ManyToManyField(User, related_name='admin_groups')
