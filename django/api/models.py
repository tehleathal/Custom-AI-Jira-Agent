from django.db import models

class ModelRequest(models.Model):
    request = models.TextField()
    response = models.TextField()
    
    def __str__(self):
        return f'Request: {self.request}\nResponse: {self.response}'
    