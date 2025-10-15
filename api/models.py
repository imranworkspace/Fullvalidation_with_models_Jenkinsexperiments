from django.db import models

# Create your models here.
class StudentModel(models.Model):
    name=models.CharField(max_length=25)
    email=models.EmailField()
    password=models.CharField(max_length=50)
    pincode = models.IntegerField(null=True, blank=True)

    dob = models.DateField(null=True, blank=True)  # Changed from CharField to DateField
    appointment_time = models.TimeField(null=True, blank=True)  # Changed to TimeField
    appointment_date = models.DateField(null=True, blank=True)  # Changed to DateField
    appointment_datetime = models.DateTimeField(null=True, blank=True)  # Changed to DateTimeField

    is_agreed = models.BooleanField(default=False)  # Keep only one "agree" field

    gender = models.CharField(max_length=36, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], null=True, blank=True)

    interests = models.CharField(max_length=100, null=True, blank=True)  # Fixed typo & increased length
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    mobile_no = models.CharField(max_length=15, null=True, blank=True)  # Could use PhoneNumberField if using django-phonenumber-field
    slug = models.SlugField(unique=True, null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)  # Or use IntegerField if only whole numbers
    content = models.TextField(null=True, blank=True)
    marriedornot = models.BooleanField(default=False)
    split_date_time = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.name