from django.contrib import admin
from .models import User, CompanyProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('company_name', 'user__username')
    actions = ['approve_companies']

    def approve_companies(self, request, queryset):
        queryset.update(is_approved=True)
    approve_companies.short_description = 'Approve selected companies'
