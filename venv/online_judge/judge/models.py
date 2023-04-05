from django.db import models


# Create your models here.
class Questions(models.Model):
    problem_id = models.IntegerField(null=False)
    problem_title = models.CharField(max_length=255)
    problem_description = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()



