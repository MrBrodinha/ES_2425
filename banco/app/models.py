# Create your models here.
from django.db import models


class People(models.Model):
    personid = models.AutoField(db_column='PersonID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'People'
