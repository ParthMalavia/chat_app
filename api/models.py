from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self) -> str:
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(default="default.jpg", upload_to="user_images", null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.full_name

    def save(self, *args, **kwargs) -> None:
        if not self.full_name:
            self.full_name = self.user.username
        return super(Profile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    message = models.CharField(max_length=250)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]
        verbose_name_plural = "Messages"

    def __str__(self) -> str:
        return f"{self.sender} - {self.receiver}"

    @property
    def sender_profile(self):
        return Profile.objects.get(user=self.sender)

    @property
    def receiver_profile(self):
        return Profile.objects.get(user=self.receiver)


