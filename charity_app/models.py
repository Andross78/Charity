from django.db import models
from django.contrib.auth.models import AbstractUser


INSTITUTION = (
    (0, 'F'),
    (1, 'OP'),
    (2, 'ZL'),
)

class User(AbstractUser):

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.IntegerField(choices=INSTITUTION, default=0)
    category = models.ManyToManyField(Category, related_name='institutions')

    def __str__(self):
        return self.name

    def get_category(self):
        output = []
        for cat in self.category.all():
            output.append(cat.name)
        return output

class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category, related_name='donations')
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    address = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=16)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=64)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    is_take = models.BooleanField(default=False)