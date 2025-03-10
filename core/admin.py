from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.http import HttpResponse
import csv
from django.db.models import Q
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin
from import_export import resources
from import_export.formats.base_formats import CSV

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_published', 'is_in_progress', 'is_completed', 'created_at')
    search_fields = ('title', 'user__email')
    list_filter = ('is_published', 'is_in_progress', 'is_completed')
    ordering = ('-created_at',)  # Order jobs from newest to oldest


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'applied_at')
    search_fields = ('user__email', 'job__title')
    list_filter = ('applied_at',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('job', 'amount', 'status', 'paid_at')
    search_fields = ('job__title', 'status')
    list_filter = ('status', 'paid_at')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)  # Show latest messages first