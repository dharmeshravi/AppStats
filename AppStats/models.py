from django.db import models
from datetime import datetime
from django.conf import settings

class AppDetail(models.Model):
    Application = models.CharField(max_length=500, blank=False, null=False)
    appEndPoint = models.URLField(max_length = 200, blank=False, null=False)
    app2Monitor = models.BooleanField(default=True)

    def __str__(self):
        return self.Application
        
    class Meta:
        managed = True
        db_table = 'appdetail'
               
class AppData(models.Model):
    application = models.ForeignKey(AppDetail, on_delete=models.CASCADE, related_name="application")
    status  = models.CharField(max_length=500, blank=False, null=False)
    status_time = models.DateTimeField(default=datetime.now())
    
    def __str__(self):
        return self.application.Application + " - " + self.status
        
    class Meta:
        managed= True
        db_table = 'appdata'

class Interface(models.Model):
    target = models.CharField(max_length=500, blank=False, null=False)
    status = models.CharField(max_length=500, blank=False, null=False)
    message= models.CharField(max_length=500, blank=False, null=False)
    targets= models.ForeignKey(AppData, on_delete=models.CASCADE, related_name='targets')
    
    def __str__(self):
        return self.target
        
    class Meta:
        managed = True
        db_table = 'interface'        