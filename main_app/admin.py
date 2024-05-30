from django.contrib import admin

from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "referrer", "password"]
    list_display_links = ["id", "username"]
    list_filter = ["referrer"]
    search_fields = ["username", "email"]
    list_per_page = 30

# class WaitingUserAdmin(admin.ModelAdmin):
#     list_display = ["id", "email", "created_at"]
#     list_display_links = ["id", "email"]
#     search_fields = ["email"]
#     list_per_page = 30

class RecommendationAdmin(admin.ModelAdmin):
    list_display = ["id", "recommended_person", "user", "email", "submitted_at"]
    list_display_links = ["id", "recommended_person"]
    list_filter = ["user"]
    search_fields = ["recommended_person", "email"]
    list_per_page = 30

admin.site.register(User, CustomUserAdmin)
# admin.site.register(WaitingUser, WaitingUserAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
