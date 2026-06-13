from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category       = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name           = models.CharField(max_length=200)
    slug           = models.SlugField(unique=True, blank=True)
    image          = models.ImageField(upload_to='products/', blank=True)
    description    = models.TextField(blank=True)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock          = models.PositiveIntegerField(default=0)
    available      = models.BooleanField(default=True)
    brand          = models.CharField(max_length=100, blank=True)
    rating         = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    rating_count   = models.PositiveIntegerField(default=0)
    is_featured    = models.BooleanField(default=False)
    is_bestseller  = models.BooleanField(default=False)
    created        = models.DateTimeField(auto_now_add=True)
    updated        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def in_stock(self):
        return self.stock > 0


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user    = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating  = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    title   = models.CharField(max_length=200)
    body    = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.username} – {self.product.name}'