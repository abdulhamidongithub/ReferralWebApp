from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True)
    referrer = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referred_users')
    referral_link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-id"]

# class WaitingUser(models.Model):
#     email = models.EmailField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.email
#
#     class Meta:
#         ordering = ["-id"]

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    recommended_person = models.CharField(max_length=255)
    email = models.EmailField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recommended_person} by {self.user.username}"

    class Meta:
        ordering = ["-id"]
