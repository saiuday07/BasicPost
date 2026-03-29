from django.db import models
from django.contrib.auth.models import User

class post(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    subtitle=models.CharField(max_length=400)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='images/') #pip install pillow

    #python manage.py makemigrations -> to create migration file
    #python manage.py migrate -> to apply the changes  or migrations to the database