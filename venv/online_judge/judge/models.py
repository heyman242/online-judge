from django.db import models


# Create your models here.
class Questions(models.Model):
    problem_id = models.IntegerField(null=False)
    problem_title = models.CharField(max_length=255)
    problem_description = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()


def __str__(self):
    return self.problem_title


class CodeSnippet(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    language = models.CharField(max_length=10)
    code = models.TextField()

    def __str__(self):
        return self.language
