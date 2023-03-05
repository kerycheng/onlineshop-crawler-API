from django.db import models

class ProductKeyword(models.Model):
    keyword = models.CharField(max_length=255)

    def __str__(self):
        return self.keyword


class Momoshop(models.Model):
    title = models.CharField(max_length=255, blank=False)
    brand = models.CharField(max_length=50, blank=False)
    link = models.URLField(max_length=200, blank=False)
    price = models.CharField(max_length=50, blank=True)
    amount = models.CharField(max_length=50, blank=False)
    cate = models.CharField(max_length=200, blank=False)
    desc = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.title
    
class Shopee(models.Model):
    title = models.CharField(max_length=255, blank=False)
    specification = models.CharField(max_length=255, blank=False)
    link = models.URLField(max_length=200, blank=False)
    price_min = models.CharField(max_length=200, blank=False)
    price_max = models.CharField(max_length=200, blank=False)
    historical_sold = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.title

class Ruten(models.Model):
    title = models.CharField(max_length=255, blank=False)
    link = models.URLField(max_length=200, blank=False)
    price_min = models.CharField(max_length=200, blank=False)
    price_max = models.CharField(max_length=200, blank=False)
    historical_sold = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.title