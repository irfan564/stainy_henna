from django.db import models


class ServiceCategory(models.Model):
    """Categories for mehandi services (e.g., Bridal, Party, Kids)."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='service_categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'
        ordering = ['name']


class Service(models.Model):
    """Individual mehandi service offerings."""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    duration = models.CharField(max_length=50, help_text='e.g., 2-3 hours')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price

    class Meta:
        ordering = ['-is_featured', 'name']
