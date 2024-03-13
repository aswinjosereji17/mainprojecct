from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# class UserProfile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     address = models.CharField(max_length=255)
#     # Other fields for user profile

#     def __str__(self):
#         return self.user.username  # Return the username as the string representation
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    hub_status = models.BooleanField(default=False) 
    # Other fields for user profile

    def __str__(self):
        return self.user.username

class UserAddress(models.Model):
    user_addr_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15, null=True)  # Allow null values for mobile number
    pincode = models.CharField(max_length=10, null=True)  # Allow null values for pincode
    district = models.CharField(max_length=100, null=True)  # Allow null values for district
    city = models.CharField(max_length=100, null=True)  # Allow null values for city
    house_name = models.CharField(max_length=255, null=True)  # Allow null values for house name

    def __str__(self):
        return f'User Address for {self.user.email}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_address(sender, instance, created, **kwargs):
    if created:
        UserAddress.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=User)
def save_user_address(sender, instance, **kwargs):
    instance.useraddress.save()

# Connect the signal handlers
post_save.connect(create_user_profile, sender=User)
post_save.connect(create_user_address, sender=User)
post_save.connect(save_user_profile, sender=User)
post_save.connect(save_user_address, sender=User)

class SellerRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
    gstin = models.CharField(max_length=15, blank=True)
    document = models.FileField(upload_to='seller_documents/', blank=True)
    company = models.CharField(max_length=100, blank=True,null=True)
    request_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



class HomeSpecialOffer(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=100)
    description = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='special_offer_images/')  # Define the image field

    def __str__(self):
        return self.prod_name



# product

class ProductCategory(models.Model):
    categ_id = models.AutoField(primary_key=True)  # Use AutoField instead of IntegerField
    categ_name = models.CharField(max_length=255, null=False, unique=True)
    categ_image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categ_name

class ProductSubcategory(models.Model):
    sub_cat_id = models.AutoField(primary_key=True)
    categ_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    sub_cat_name = models.CharField(max_length=255,unique=True)
    subcat_image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.sub_cat_name

class Fish(models.Model):
    fish_id = models.AutoField(primary_key=True)
    fish_name = models.CharField(max_length=255)
    

    def __str__(self):
        return self.fish_name

from django.db import models


class Product(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=255, null=False, unique=True)
    # fish_name = models.ForeignKey(Fish, on_delete=models.CASCADE)
    sub_categ_id = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Use Django's default user model
    stock_quantity = models.PositiveIntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.prod_name


class ProductDescription(models.Model):
    prod_desc_id = models.AutoField(primary_key=True)
    prod_id = models.OneToOneField(Product, on_delete=models.CASCADE,unique=True)
    description = models.TextField(null=False)
    img1 = models.ImageField(upload_to='product_images/', null=False)
    img2 = models.ImageField(upload_to='product_images/', null=False)
    img3 = models.ImageField(upload_to='product_images/', null=False)
    instructions = models.TextField(null=False)

    def __str__(self):
        return f"Description for {self.prod_id.prod_name}"


class AddCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)  # Using the User model from Django's auth module
    cart_date = models.DateTimeField(auto_now_add=True) 

class CartItems(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(AddCart, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming you have a Product model
    quantity = models.IntegerField()
    cart_item_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Set a default value of 0.0

    def save(self, *args, **kwargs):
        # Calculate the total price based on the quantity and the price of the associated product
        if self.prod:
            self.total_price = self.quantity * self.prod.price  # Assuming 'price' is a field in your Product model
        super().save(*args, **kwargs)




class Wishlist(models.Model):
    wish_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you're using Django's built-in User model
    wishlist_date = models.DateTimeField(auto_now_add=True) 
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Wishlist Item {self.wish_id}'




class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    outof_rating = models.IntegerField(default=5, editable=False)
    description = models.TextField()
    sentiment_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username}"


class ProductRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    requested_user = models.ForeignKey(User, on_delete=models.CASCADE)
    categ_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_request_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request ID: {self.request_id}, Product: {self.product_name}, Requested by: {self.requested_user}"


class Order(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)  # Assuming you have a Product model
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=255, default=None)
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    all_received = models.BooleanField(default=False)  # New field

    def str(self):
        return self.user.username 

    def update_all_received_status(self):
        # Check if all OrderNotification_Seller objects associated with this order have 'SU' status
        all_received = all(notification.shipped == 'SU' for notification in self.ordernotification_seller_set.all())
        self.all_received = all_received
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calculate the total price for this order item based on quantity and price
        self.total_price = self.quantity * self.price
        super(OrderItem, self).save(*args, **kwargs)
        
        # Update the total order price in the associated Order model
        order = self.order
        order.total_order_price = sum(order_item.total_price for order_item in order.orderitem_set.all())
        order.save()

class OrderNotification_Seller(models.Model):
    ORDER_REQUESTED = 'OR'
    DELIVERED = 'DL'
    SUCCESSFUL = 'SU'
    
    SHIPPED_CHOICES = [
        (ORDER_REQUESTED, 'Order Requested'),
        (DELIVERED, 'Delivered'),
        (SUCCESSFUL, 'Successful'),
    ]

    KERALA_DISTRICTS = {
        'Thiruvananthapuram', 'Kollam', 'Pathanamthitta', 'Alappuzha', 'Kottayam', 'Idukki',
        'Thrissur', 'Palakkad', 'Malappuram', 'Kozhikode',
        'Kasaragod', 'Kannur', 'Wayanad'
    }

    HUB_MAP = {
        'Pathanamthitta': 'Pathanamthitta',
        'Alappuzha': 'Pathanamthitta',
        'Kollam': 'Pathanamthitta',
        'Thiruvananthapuram': 'Pathanamthitta',
        'Kottayam': 'Pathanamthitta',
        'Idukki': 'Pathanamthitta',
        'Thrissur': 'Malappuram',
        'Palakkad': 'Malappuram',
        'Malappuram': 'Malappuram',
        'Kozhikode': 'Malappuram',
        'Kasaragod': 'Kannur',
        'Kannur': 'Kannur',
        'Wayanad': 'Kannur'
    }

    notif_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=100)
    prod_cat = models.CharField(max_length=100,null=True)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(OrderItem, on_delete=models.CASCADE, default=None, null=True)
    main_order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None, null=True)
    stored_tank = models.CharField(max_length=100, default=None, blank=True, null=True)
    
    seller_name = models.ForeignKey(User, on_delete=models.CASCADE)
    noti_date = models.DateField(auto_now_add=True)
    shipped = models.CharField(max_length=2, choices=SHIPPED_CHOICES, default=ORDER_REQUESTED)
    district = models.CharField(max_length=100, null=True)
    hub = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.prod_name} - {self.get_shipped_display()}'

    def save(self, *args, **kwargs):
        if self.district in self.KERALA_DISTRICTS:
            self.hub = self.HUB_MAP.get(self.district)
        super().save(*args, **kwargs)
        
        if self.shipped == 'SU' and self.main_order:
            self.main_order.update_all_received_status()  

class Event(models.Model):
    MODE_CHOICES = (
        ('offline', 'Offline'),
        ('online', 'Online'),
    )
    event_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    event_img = models.ImageField(upload_to='events/', null=False)
    date = models.DateField()
    description = models.TextField()
    mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    duration = models.CharField(max_length=255, null=True)
    booking_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

from datetime import timedelta
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Subscription(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=255, default=None)
    payment_status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.payment_status == self.PaymentStatusChoices.SUCCESSFUL:
            self.payment_date = timezone.now()
            # Set expiration date to 28 days from the payment date
            self.expiration_date = self.payment_date + timedelta(days=1)
            
        elif self.payment_status == self.PaymentStatusChoices.FAILED or self.payment_status == self.PaymentStatusChoices.PENDING:
            # If payment failed or is pending, reset payment_date and expiration_date
            self.payment_date = None
            self.expiration_date = None
            self.status = False

        # Explicitly set status to False if both expiration_date and payment_date are None
        if self.expiration_date is None and self.payment_date is None:
            self.status = False
        elif self.expiration_date and timezone.now() > self.expiration_date:
            # If the current time is past the expiration date, set status to False
            self.status = False
        else:
            # Otherwise, the subscription is considered active
            self.status = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username





class Subscription_details(models.Model):
    sub_name = models.CharField(max_length=255)
    sub_image = models.CharField(max_length=255)
    sub_amount = models.FloatField()
    sub_offer1 = models.CharField(max_length=255)
    sub_offer2 = models.CharField(max_length=255)
    sub_offer3 = models.CharField(max_length=255)

    def __str__(self):
        return self.sub_name


class CommunityPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    likes = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading


class PostLikes(models.Model):
    like_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(CommunityPost, on_delete=models.CASCADE)
    liked_user = models.ForeignKey(User, on_delete=models.CASCADE)
    # likes = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post_id', 'liked_user')  # Ensures each user can like a post only once

    def __str__(self):
        return f"Like: {self.like_id} - Post: {self.post_id} - Liked by: {self.liked_user}"


from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'{self.user.username} - {self.message}'