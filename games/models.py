from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User, Group

#user_group = Group.objects.create(name='user')
#manager_group = Group.objects.create(name='manager')
#admin_group = Group.objects.create(name='admin')


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()
    discount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    type = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    @property
    def discount_price(self):
        return float(self.price) * (1 - float(self.discount) / 100)

