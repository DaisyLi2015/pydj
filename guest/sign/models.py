from django.db import models

# Create your models here.

# event table
class Event(models.Model):

    name = models.CharField(max_length=100) #event title
    limit = models.IntegerField()           #amount of attendance people
    status = models.BooleanField()          #status of event
    address = models.CharField(max_length=200) #address
    start_time = models.DateTimeField('events time') #time of event
    create_time = models.DateTimeField(auto_now=True) #create time of event(auto)

    def __str__(self):
        return self.name

class Guest(models.Model):

    event = models.ForeignKey(Event)  # id of event foreignkey
    realname = models.CharField(max_length=64) #name of guest
    phone = models.CharField(max_length=16)  #phone of guest
    email = models.EmailField()   #email of guest
    sign = models.BooleanField() #status of sign
    create_time = models.DateTimeField(auto_now=True)

    class Meta: # event_id+phone as unique primary key
        unique_together = ("event","phone")

    def __str__(self):    # tell python will return object as str
        return self.realname