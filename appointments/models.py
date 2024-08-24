from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


class User(AbstractUser):
    nic_number = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=11, unique=True)
    is_doctor = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    nic_number = models.CharField(max_length=20, unique=True)
    is_doctor = models.BooleanField(default=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} - {self.doctor.name} - {self.user.username}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('confirmed', 'Confirmed'),
        ('denied', 'Denied'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='requested')

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.name} on {self.date} at {self.time}"

    def clean(self):
        overlapping_appointments = Appointment.objects.filter(
            doctor=self.doctor,
            date=self.date,
            time__gte=(datetime.combine(self.date, self.time) - timedelta(hours=1)).time(),
            time__lte=(datetime.combine(self.date, self.time) + timedelta(hours=1)).time(),
        ).exclude(pk=self.pk)
        if overlapping_appointments.exists():
            raise ValidationError("The doctor already has an appointment at this time. Please choose another time.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
