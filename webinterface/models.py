from django.db import models

class Sequence(models.Model):
    species = models.CharField(max_length=255)
    gene_id = models.CharField(max_length=255)
    sequence = models.TextField()
    value = models.FloatField()

    def __str__(self):
        return self.gene_id
