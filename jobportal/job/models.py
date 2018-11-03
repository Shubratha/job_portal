from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=200, default='fname')
    last_name = models.CharField(max_length=200, default='lname')
    username = models.CharField(max_length=200, Unique=True)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=500)
    user_type = models.CharField(max_length=200)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.first_name
        self.last_name
         self.username
         self.password
        self.username
         self.username
         self.user_type
        }
