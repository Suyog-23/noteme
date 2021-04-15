from django.db import models

# Create your models here.
class Contact(models.Model):
    subject = models.CharField(max_length=200, default='')
    email = models.EmailField(default='')
    description = models.TextField(default='', max_length=3000)

    def __str__(self):
        return self.subject + ' | ' + self.email

class Lectures(models.Model):
    subject = models.CharField(max_length=200, default='Add here')
    date_uploaded = models.DateField(auto_now_add=True)
    notes = models.TextField(default='')
    
    def __str__(self):
        return self.subject + ' | ' + str(self.date_uploaded)
    