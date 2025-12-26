from django.contrib import admin
from .models import Students, GuestBooking


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'age')
	search_fields = ('name',)


@admin.register(GuestBooking)
class GuestBookingAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'email', 'room_requested', 'status', 'created_at')
	list_filter = ('status', 'created_at')
	search_fields = ('name', 'email', 'room_requested')
	ordering = ('-created_at',)