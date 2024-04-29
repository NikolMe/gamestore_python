from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User, Group


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
    description = models.TextField(default='')
    description_uk = models.TextField(default='')
    description_fr = models.TextField(default='')
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

    def get_description(self, request):
        if request.LANGUAGE_CODE == 'en':
            return self.description
        elif request.LANGUAGE_CODE == 'fr':
            return self.description_fr
        elif request.LANGUAGE_CODE == 'uk':
            return self.description_uk
        else:
            return self.description
