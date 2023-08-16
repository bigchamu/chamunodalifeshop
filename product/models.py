# Form Images
from io import BytesIO
from os import name
from PIL import Image
from django.core.files import File
from django.db.models import Sum
from django.db import models
from vendor.models import Vendor


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name="products", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True) # Change uploads to thumbnails 

    class Meta:
        ordering = ['-added_date']

    def __str__(self):
        return self.title

    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            
            else:
                # Default Image
                return 'https://via.placeholder.com/240x180.jpg'
    
    @staticmethod
    def getFeaturedProducts():
        return [featured.product for featured in FeaturedProduct.objects.all().order_by('created')[:3]]
    
    # Generating Thumbnail - Thumbnail is created when get_thumbnail is called
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    
    def get_number_of_reviews(self) -> int:
        return Review.objects.filter(product=self).count()
    
    def getRating(self) -> float:
        return int(Review.objects.filter(product=self).aggregate(Sum('rating'))['rating__sum'] / self.get_number_of_reviews())

    def get_rating_raw_html(self):  
        star = """<i class="text-warning fa fa-star"></i>"""
        muted = """<i class="text-muted fa fa-star"></i>"""
        num_stars = self.getRating()
        num_muted = 5 - num_stars
        res = ""
        for i in range(num_stars):
            res += star
        for i in range(num_muted):
            res += muted
        return res
class FeaturedProduct(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.OneToOneField(Product,null=False,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True,null=False)

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product,null=False,on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    rating = models.FloatField(default=5,null=False)
