from django.contrib import admin
from .models import User, Profile, ChatMessage

class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ["verified", "full_name"]
    list_display = ["user", "full_name", "verified"]


class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ["is_read"]
    list_display = ["sender", "receiver", "message", "is_read"]


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)

