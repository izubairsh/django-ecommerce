from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)
    quantity = models.IntegerField(default=1,)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    token = models.IntegerField(unique=True, null=True, blank=True)
    cost = models.IntegerField()
    price = models.IntegerField()
    weight = models.IntegerField()
    meat = models.IntegerField()
    quantity = models.IntegerField(default=1,)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    expense = models.BooleanField(default=False)

    def __str__(self):
        return str(self.token)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        try:
            this = Product.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
        except:
            pass
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']
