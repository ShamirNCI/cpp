# Create your models here.
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

ASSET_CHOICES = (
    ("Electrical", "Electrical"),
    ("Civil", "Civil"),
    ("Mechanical", "Mechanical"),
    ("Spare","Spare"),
    ("Other","Other"), 
)
ASSET_LOCATION  = (
    ("Level-1","Level-1"),
    ("Level-2","Level-2"),
    ("Level-3","Level-3"),
    ("Level-4","Level-4"),
)
ASSET_LOCATION  = (
    ("Level-1","Level-1"),
    ("Level-2","Level-2"),
    ("Level-3","Level-3"),
    ("Level-4","Level-4"),
)

class Asset(models.Model):
    asset_id = models.AutoField(primary_key=True)
    asset_name = models.CharField(max_length=100)
    asset_desc = models.CharField(max_length=100)
    asset_loc = models.CharField(max_length=100, choices=ASSET_LOCATION)
    asset_tag = models.CharField(max_length=100)
    #make model
    asset_group = models.CharField(max_length=100)
    asset_category = models.CharField(max_length=100, choices=ASSET_CHOICES)
    asset_serial_No = models.CharField(max_length=100)
    asset_manufacturer = models.CharField(max_length=100)
    date_purchased = models.DateTimeField()
    date_warranty = models.DateTimeField()
    asset_warranty = models.BooleanField(default=False)
    asset_active = models.BooleanField(default=False)
    asset_Maintainable  = models.BooleanField(default=False)
    #asset_image = models.ImageField(default="default.jpeg", upload_to = 'images/')
    asset_main_date = models.DateField()

    def __str__(self):
        return self.asset_name

class AssetMain(models.Model):
    #asset_main_id = models.AutoField(primary_key=True)
    asset_id = models.CharField(max_length=100)
    asset_name = models.CharField(max_length=100)
    asset_tag = models.CharField(max_length=100)
    asset_serial_No = models.CharField(max_length=100)
    asset_loc = models.CharField(max_length=100)
    asset_status = models.CharField(max_length=100,null=True, default=None, blank=True)
    date_main = models.DateTimeField(blank=True, null=True,default=datetime.date.today)
    asset_desc = models.CharField(max_length=100,null=True, default=None, blank=True)
    asset_assign = models.CharField(max_length=100,null=True, default=None, blank=True)
    date_solved = models.DateTimeField(null=True, default=None, blank=True)
    asset_comments = models.CharField(max_length=100,null=True, default=None, blank=True)
    def __str__(self):
        return self.asset_name
    

class Bus(models.Model):
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.bus_name


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    userid =models.DecimalField(decimal_places=0, max_digits=2)
    busid=models.DecimalField(decimal_places=0, max_digits=2)
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=2)

    def __str__(self):
        return self.email
