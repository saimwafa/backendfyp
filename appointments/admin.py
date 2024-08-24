# appointments/admin.py

from django.contrib import admin
from .models import User, Doctor, Review

# Customizing the User admin to display the new location field
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'nic_number', 'is_doctor', 'location')  # Display these fields in the list view
    search_fields = ('username', 'email', 'phone', 'nic_number', 'location')  # Enable search by these fields
    list_filter = ('is_doctor',)  # Filter by the is_doctor field

# Customizing the Doctor admin to display the new location field
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'speciality', 'nic_number', 'location')  # Display these fields in the list view
    search_fields = ('name', 'email', 'phone', 'speciality', 'nic_number', 'location')  # Enable search by these fields
    list_filter = ('speciality',)  # Filter by the speciality field

# Customizing the Review admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'user', 'rating', 'created_at')  # Display these fields in the list view
    search_fields = ('doctor__name', 'user__username', 'rating', 'comment')  # Enable search by these fields
    list_filter = ('rating', 'created_at')  # Filter by the rating and created_at fields

# Alternatively, you can use the simpler approach as you originally did with slightly enhanced functionality:
# admin.site.register(User, UserAdmin)
# admin.site.register(Doctor, DoctorAdmin)
# admin.site.register(Review, ReviewAdmin)
