from django.db import models

class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=255, unique=True)  # Asegúrate de que sea único y no nulo
    description = models.TextField()
    severity = models.CharField(max_length=50)
    fixed = models.BooleanField(default=False)

    def __str__(self):
        return self.cve_id
