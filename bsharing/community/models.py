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

class post_type_header(models.Model):
    post_community = models.ForeignKey("community.community_header", on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    desc = models.TextField()
    semantic_tag = models.CharField(max_length = 150)

    
    def __str__(self):
        return self.name + "--" + self.desc


