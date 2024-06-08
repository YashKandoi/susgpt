from django.db import models

class Website(models.Model):
    company_name = models.CharField(max_length=100)
    url = models.URLField()
    output = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name + ' '
