from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    symptoms = models.TextField()
    signature_data = models.TextField(blank=True, null=True) # Signature base64 format lo store avtundi
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name