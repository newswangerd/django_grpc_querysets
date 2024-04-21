from django.db import models

# Create your models here.


class TestOneToMany(models.Model):
    name = models.CharField(max_length=255)


class TestModel(models.Model):
    name = models.CharField(max_length=255)
    f1 = models.CharField(max_length=255, null=True)
    f2 = models.CharField(max_length=255, null=True)
    my_fk = models.ForeignKey(TestOneToMany, on_delete=models.CASCADE, null=True)


class TestManyToOne(models.Model):
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE)
