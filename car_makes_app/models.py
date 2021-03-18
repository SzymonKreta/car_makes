from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Car(models.Model):
    make = models.CharField(max_length=120, help_text="str: car make")
    model = models.CharField(max_length=150, help_text="str: car model")

    def save(self, *args, **kwargs):
        self.make = self.make.lower()
        self.model = self.model.lower()
        return super(Car, self).save(*args, **kwargs)


class Rate(models.Model):
    car = models.ForeignKey(to=Car, on_delete=models.DO_NOTHING, null=True, help_text="car")
    rate = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)],
                               help_text="str: car model rate")
