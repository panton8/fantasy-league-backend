from django.contrib import admin

from user.models import StaffUser, User
from user.models import UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...


@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    ...


@admin.register(UserProfile)
class StaffUserAdmin(admin.ModelAdmin):
    ...