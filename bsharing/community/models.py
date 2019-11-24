from django.db import models
from django.urls import reverse


# Create your models here.

class community_header(models.Model):
    user_name = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    desc = models.TextField()
    semantic_tag = models.CharField(max_length = 150)

    def __str__(self):
        return self.name + "--" + self.desc

    def get_absolute_url(self):
        return reverse('community:community_detail', kwargs={"pk" : self.pk})



class define_post_types(models.Model):

    Audio = 'AU'
    Text = 'TX'
    Image = 'IM'
    Integer = 'INT'
    Date = 'DATE'
    Video = 'VIDEO'
    Email = 'EM'
    Location = 'LOC'
    URL = 'URL'

    Fieldtypes = [
        (Audio, 'Audio'),
        (Text, 'Text'),
        (Image, 'Image'),
        (Integer,'Integer'),
        (Date, 'Date'),
        (Video, 'Vide'),
        (Email, 'E-mail'),
        (Location, 'Location'),
        (URL, 'URL'),
    ]    
    community = models.ForeignKey(community_header, default="", on_delete=models.CASCADE)
    label_name = models.CharField(max_length=100)
    label_structure = models.CharField(max_length = 10, choices=Fieldtypes, default=Text)
    label_isrequired = models.BooleanField(default=False)

    def __str__(self):
      return self.label_name #+ '-' + self.label_structure + '-' + self.label_isrequired

class post_type_header(models.Model):
    post_community = models.ForeignKey(community_header, default="", on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    desc = models.TextField()
    semantic_tag = models.CharField(max_length = 150)
    fields = models.ManyToManyField(define_post_types)
    
    def __str__(self):
      return self.name + "--" + self.desc

    def get_absolute_url(self):
        return reverse('community:post_type_form', kwargs= {"pk" : self.pk})
