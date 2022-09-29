from django.db import models

# Create your models here.
class EmailData(models.Model):
    _from = models.EmailField()
    subject = models.CharField(max_length=255,blank=True)
    body = models.TextField()
    
    def __str__(self):
        return self._from