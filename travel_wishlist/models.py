from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

# Create your models here.
#cascade = delete all related places
# Textfield = can have as many 
#childfield = has a limit
class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=200)   
    visited = models.BooleanField(default=False)  
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True) #  validators=[validate_date_today_or_in_past])
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    #this will override and django save method call throuhgt actual data 

    def save(self, *args, **kwargs):
        old_place = Place.objects.filter(pk=self.pk).first()
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo) 

        super().save(*args, **kwargs) # excuted the save

                # if oldplace has a photo and thea oldphoto is different than new than # delete photo

    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

            # override the delete option 

    def delete(self, *args, **kwargs):
        if self.photo:
             self.delete_photo(self.photo) 

        super().delete(*args, **kwargs) # excuted the delete


    def __str__(self): # string method  
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100] if self.notes else 'No notes'
        return f'{self.name}, visited? {self.visited} on {self.date_visited}. Notes: {notes_str}.'  # this will not display to the user 


