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
    LANGUAGE_CHOICES = [
        ('cpp', 'C++'),
        ('python', 'Python'),
        ('java', 'Java'),

    ]
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    code = models.TextField()

    def __str__(self):
        return self.code


class test_cases(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    inputs = models.JSONField()
    outputs = models.JSONField()

    # def __str__(self):
    #     return f"{self.question} - inputs: {json.dumps(self.inputs)}, outputs: {json.dumps(self.outputs)}"

# With this implementation, when you call str(test_case), it will return a string representation of the test case with the inputs and outputs fields as JSON strings.
