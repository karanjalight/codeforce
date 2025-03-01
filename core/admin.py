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



def export_students_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Gender', 'NPI', 'Date of Birth', 'Class', 'Is Active', 'Parents', 'Date Joined'])

    for student in queryset:
        parents = ", ".join([parent.email for parent in student.parents.all()])
        writer.writerow([student.name, student.get_gender_display(), student.npi, student.dob, student.students_class, student.is_active, parents, student.date_joined])

    return response

export_students_csv.short_description = "Export selected students to CSV"


class StudentAdminForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'


    
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        import_id_fields = ('npi',)  # Adjust according to your model's unique identifier

class StudentAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    form = StudentAdminForm
    list_display = ('name', 'npi', 'gender', 'students_class', 'is_active', 'get_age')
    list_filter = ('gender', 'students_class', 'is_active', 'date_joined', 'type')
    search_fields = ('name', 'admission_number', 'students_class__name', 'parents__email')
    filter_horizontal = ('parents',)
    readonly_fields = ('payments',)  # Make payments read-only
    fieldsets = (
        (None, {
            'fields': ('name', 'admission_number', 'profile_pic', 'type', 'gender', 'dob', 'npi', 'students_class', 'is_active', 'date_joined')
        }),
        ('Additional Info', {
            'fields': ('about_student', 'parents', 'payments')
        }),
    )
    resource_class = StudentResource
    formats = [CSV]  # Specify formats you want to support

    def get_age(self, obj):
        return obj.get_age()
    get_age.short_description = 'Age'

    search_fields = ('npi', 'name', 'type')
    ordering = ('students_class__grade__name',) 
    
      
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'student', 'term', 'amount', 'balance', 'service_fee', 'date_created', 'is_active')
    list_filter = ('term', 'is_active', 'date_created')
    search_fields = ('name', 'user__email', 'student__name')
    filter_horizontal = ('amount_paid',)

class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'start_date', 'end_date', 'fee_deadline', 'fee_amount')
    list_filter = ('year', 'start_date', 'end_date')
    search_fields = ('name', 'year')

class FeeAdmin(admin.ModelAdmin):
    list_display = ('student_class', 'grade', 'date_created', 'type', 'amount')  # Fields to display in the admin list view
    search_fields = ('student_class', 'grade__name')  # Enable search by student class and grade name
    list_filter = ('type', 'date_created')  # Enable filtering by type and date created
    ordering = ('grade__name',)  # Order by the name field of the grade related model

    
class AmountPaidAdmin(admin.ModelAdmin):
    # List display to show these fields in the admin list view
    list_display = ('ref_code', 'user', 'amount', 'date')
    
    # List filter to filter by user and date
    list_filter = ('user', 'date')
    
    # Search fields to enable search functionality
    search_fields = ('ref_code', 'user__username', 'user__email')
    
    # Read-only fields to prevent modification of certain fields
    readonly_fields = ('id', 'date')
    
    # Fields to be displayed in the form view
    fields = ('ref_code', 'user', 'amount', 'date')
    
    # Ordering of the list view
    ordering = ('-date',)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
    

class StudentClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp')  # Fields to display in the admin list view
    search_fields = ('name',)  # Fields to search in the admin list view
    list_filter = ('timestamp',)  # Fields to filter in the admin list view


# Register the admin class with the associated model
admin.site.register(Student, StudentAdmin)
admin.site.register(AmountPaid, AmountPaidAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(StudentClass, StudentClassAdmin)