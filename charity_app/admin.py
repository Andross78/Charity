from django.contrib import admin

from .models import Donation, Category, Institution, User

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    ...

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    ...

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...