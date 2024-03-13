from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import UserProfile, Product, SellerRequest, HomeSpecialOffer, ProductCategory,UserAddress, Wishlist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.db.models import Avg
from .models import Product, Review
from django.db.models import Sum




# Create your views here.
@never_cache
def index(request):
    homeimg = HomeSpecialOffer.objects.all()  
  
    recent_products = Product.objects.all().order_by('-created_at')[:12]
    product_ratings = []

    products_with_sentiment_sum = Product.objects.annotate(sentiment_sum=Avg('review__sentiment_score')).order_by('-sentiment_sum')[:6]

    for product in recent_products:
        avg_rating = Review.objects.filter(prod=product).aggregate(Avg('rating'))['rating__avg'] or 0
        print(avg_rating)
        product_ratings.append({'product': product, 'avg_rating': avg_rating})

    
    if request.user.is_authenticated:
        user=request.user
      
        context = {
        'homeimg': homeimg,
        'recent_products': recent_products,
        'product_ratings': product_ratings,
        'products_with_sentiment_sum': products_with_sentiment_sum
        }
        
        return render(request,'index.html', context)
    else:
        context = {
        'homeimg': homeimg,
        'recent_products': recent_products,
        'product_ratings': product_ratings,
        'products_with_sentiment_sum': products_with_sentiment_sum
        }
        
        return render(request,'index.html', context)
    
@never_cache
def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username_or_email = request.POST['username']
        password = request.POST['password'] 
        if "@" in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(username=username_or_email, password=password)
            
        if user is not None:
            login(request, user)
            if user.is_staff :
                return redirect('user_profile_view')
            elif not user.is_staff and not user.is_superuser:
                return redirect('index')
            # if user.is_staff:
            #     return redirect('user_profile_view')
           
            # else:
            #     return redirect('index')
            # return redirect('user_profile_view')
        else:
            messages.info(request, "Invalid Login")
            error_message = "Invalid Login "
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')




@never_cache  
def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.info(request,"Username Already Exists")
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"Email Already Exists") 
            return redirect('register')
        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            # UserProfile.objects.create(user=user, mobile="")
            # UserAddress.objects.create(user=user,address1="",address2="")
            success_message = "Registration successful. You can now log in."
            messages.success(request, success_message)
            return redirect('login_user')
           
    else:
        return render (request, "register.html")

@never_cache
def seller_register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username Already Exists")
            return redirect('seller_register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email Already Exists")
            return redirect('seller_register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            # user.save()
            company=request.POST['company']
            gstin = request.POST['gstin']
            document = request.FILES.get('document')
            seller_request = SellerRequest.objects.create(user=user,company=company, gstin=gstin, document=document)
            success_message = "Seller request submitted. Please wait for approval."
            # UserProfile.objects.create(user=user, mobile="")
            # UserAddress.objects.create(user=user,address1="",address2="")  
            user.save()
         
            return redirect('login_user')
           
    else:
        return render(request, "seller_reg.html")

@login_required
@never_cache

def loggout(request):
    # print('Logged Out')
    logout(request)
    return redirect('index')


from django.shortcuts import render
from .models import UserProfile,Product, ProductSubcategory, UserAddress, Product
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Count
import datetime
from django.db import models 
from django.views.decorators.cache import never_cache

# def user_profile_view(request):
#     user_profile = UserProfile.objects.get(user=request.user)
    
#     context = {
#         'user_profile': user_profile,
#     }
#     return render(request, 'user_profile.html', context)
@login_required
@never_cache
def user_profile_view(request):

    if not request.user.is_authenticated:
        return redirect('login_user')
    # user_profile = UserProfile.objects.get(user=request.user)
    user_count = User.objects.filter(is_staff=False).count()
    seller_count = User.objects.filter(Q(is_staff=True) & Q(is_superuser=False)).count()
    prod_count = Product.objects.count()
    user_products_count = Product.objects.filter(user_id=request.user).count()
    s_req= SellerRequest.objects.all()
    products_with_sentiment_sum = Product.objects.annotate(sentiment_sum=Avg('review__sentiment_score')).order_by('-sentiment_sum')[:5]
    show_orders_count = Order.objects.filter(payment_status=Order.PaymentStatusChoices.SUCCESSFUL).count()
    show_sub_count = Subscription.objects.filter(status=True).count()
    show_hub_count = UserProfile.objects.filter(hub_status=True).count()




    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None

    # try:
    #     product = Product.objects.filter(user_id=request.user)
    # except Product.DoesNotExist:
    #     product = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    context = {
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        'user_count' : user_count,
        'seller_count' : seller_count,
        'prod_count' : prod_count,
        's_req' : s_req,
        'user_products_count': user_products_count,
        'products_with_sentiment_sum': products_with_sentiment_sum,
        'show_orders_count': show_orders_count,
        'show_sub_count':show_sub_count,
        'show_hub_count':show_hub_count
        # 'product' :product
    }
    
    return render(request, 'user_prof.html', context)


from django.shortcuts import render, redirect
from .models import UserProfile, UserAddress,SellerRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


# 4-09-2023
@login_required
@never_cache
def edit_profile(request):
    if request.method == 'POST':
        # Get the current user's profile
        user_profile = UserProfile.objects.get(user=request.user)
        user = User.objects.get(username=request.user)
        user_addr= UserAddress.objects.get(user=request.user)

        # Update the profile fields with the submitted form data
        # user_profile.mobile = request.POST.get('mobile')
        # user_profile.save()
        # user_profile.profile_image=request.POST.get('prof_image')
        uploaded_image = request.FILES.get('img1')

        if uploaded_image:
            # Update the user's profile image
            user_profile.profile_image = uploaded_image
        
        user_profile.save()
        

        user_addr.address1=request.POST.get('address1')
        user_addr.address2=request.POST.get('address2')
        user_addr.save()

        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        # user.email=request.POST.get('email')
        user.save()

        # seller_req.company=request.POST.get('company')
        # seller_req.save()
        if request.user.is_staff and not request.user.is_superuser :
            # Get or create a SellerRequest object
            seller_req=SellerRequest.objects.get(user=request.user)
            seller_req.company = request.POST.get('company')
            seller_req.save()  
        # if 'profile_image' in request.FILES:
        #     user_profile.profile_image = request.FILES['profile_image']
        #     user_profile.save()

        
        # Redirect to a success page or profile page
        # return redirect('user_profile_view')
        # show_main2 = True

    # Redirect to 'user_profile_view' with the context variable
        # return render(request, 'user_prof.html', {'show_main2': show_main2})

        return redirect('user_profile')

    # If the request method is GET, render the edit profile form
 


# @login_required
# def create_product(request):
#     if request.method == 'POST':
#         prod_name = request.POST.get('prod_name')
#         sub_categ_id = request.POST.get('sub_categ_id')  # Assuming you get subcategory ID from the form
#         price = request.POST.get('price')

#         # Get the currently logged-in user
#         user = request.user

#         # Create a new product with the logged-in user
#         product = Product(
#             prod_name=prod_name,
#             sub_categ_id=sub_categ_id,
#             price=price,
#             user_id=user
#         )
#         product.save()

#         return redirect('product_list')  # Redirect to a product list view

#     return render(request, 'create_product.html')


# product



# def product_list(request):
#     query = request.GET.get('q')
#     products = Product.objects.filter(user_id=request.user)

#     if query:
#         products = products.filter(Q(prod_name__icontains=query))

#     return render(request, 'user_prof.html', {'products': products, 'query': query})





# product

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductSubcategory, ProductDescription,Fish

@login_required
@never_cache

def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.filter(user_id=request.user)
    user_profile = UserProfile.objects.get(user=request.user)
    seller_request = SellerRequest.objects.get(user=request.user)
    user_addr = UserAddress.objects.get(user=request.user)

    if query:
        products = products.filter(Q(prod_name__icontains=query))

    return render(request, 'product\product_list.html', {'products': products, 'query': query , 'user_profile': user_profile, 'seller_request': seller_request,'user_addr' : user_addr})



from django.db import IntegrityError

@login_required
@never_cache
def add_product(request):
    users = User.objects.all()
    seller_requests = SellerRequest.objects.all()
    fish=Fish.objects.all()
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    subcategories = ProductSubcategory.objects.all()

    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        'seller_requests' : seller_requests,
        'subcategories': subcategories,
        'fish' :fish,
    }

    if request.method == 'POST':
        product_name = request.POST['product_name']
        # fish = request.POST['fish']
        subcategory_id = request.POST['subcategory']
        price = request.POST['price']
        quantity=request.POST['quantity']
        description = request.POST['description']
        # instruction = request.POST['instruction']
        img1 = request.FILES['img1']
        img2 = request.FILES['img2']
        img3 = request.FILES['img3']

        # Check if the product name already exists
        if Product.objects.filter(prod_name=product_name).exists():
            # Handle the case where the product name already exists
            return HttpResponse("Product with this name already exists.")

        subcategory = ProductSubcategory.objects.get(pk=subcategory_id)
        # fish1=Fish.objects.get(pk=fish)
        
        # Create and save the product using the provided data
        product = Product(
            prod_name=product_name,
            # fish_name=fish1,
            sub_categ_id=subcategory,
            price=price,
            stock_quantity=quantity,
            user_id=request.user
        )
        product.save()

        # Create and save the product description with images
        product_description = ProductDescription(
            prod_id=product,
            description=description,
            img1=img1,
            img2=img2,
            img3=img3,
            # instructions=instruction
        )
        product_description.save()

        return redirect('product_list')  # Redirect to a product list view
    
    return render(request, 'product\save_product.html', context)


from .models import ProductSubcategory

def subcategories_view(request, categ_id):

    subcategories = ProductSubcategory.objects.filter(categ_id=categ_id)

    if request.user.is_authenticated:
        user = request.user.id
        cart = AddCart.objects.get(user=user)
        cart_items = CartItems.objects.filter(cart=cart)
        cart_item_count = cart_items.count()
        user_id = request.user.id 
        wish_count = Wishlist.objects.filter(user_id=user_id).count()

        return render(request, 'product/subcategory_list.html', {
        'subcategories': subcategories,
        'cart_item_count': cart_item_count,
        'wish_count': wish_count,
        })
    else:
        return render(request, 'product/subcategory_list.html', {
        'subcategories': subcategories,
        })

from django.shortcuts import render
from .models import Product,ProductDescription


def subcategory_products_view(request, subcat_id):
    products = Product.objects.filter(sub_categ_id=subcat_id)
    print("sssss",subcat_id)
    s_id= subcat_id

    for product in products:
            # Retrieve all reviews for the product
        reviews = Review.objects.filter(prod=product)

            # Calculate the average rating for the product
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

            # Add the average rating to the product object
        product.avg_rating = avg_rating
    
    if request.user.is_authenticated:
        user = request.user.id
        cart = AddCart.objects.get(user=user)
        cart_items = CartItems.objects.filter(cart=cart)
        cart_item_count = cart_items.count()
        user_id = request.user.id 
        wish_count = Wishlist.objects.filter(user_id=user_id).count()
    
        return render(request, 'product/products.html', {'s_id':s_id,'products': products,'cart_item_count': cart_item_count,
        'wish_count': wish_count})
    
    else:
        return render(request, 'product/products.html', {'products': products})
        

from django.db.models import Avg
def prod_desc(request, prod_id):
    # products = Product.objects.get(prod_id=prod_id)
    
   
    # return render(request, 'product/product_desc.html', {'products': products})
    # has_reviewed = Review.objects.filter(prod_id=prod_id, user=request.user).exists()
    product = get_object_or_404(Product, prod_id=prod_id)
    reviews = Review.objects.filter(prod=product)
    avg_rating = Review.objects.filter(prod=product).aggregate(Avg('rating'))['rating__avg'] or 0
    try:
        products = Product.objects.get(prod_id=prod_id)
    except Product.DoesNotExist:
        products = None

    try:
        prod_desc = ProductDescription.objects.get(prod_id=prod_id)
    except ProductDescription.DoesNotExist:
        prod_desc = None


    # user_has_purchased_product = False
    user_has_reviewed_product = False
    if request.user.is_authenticated:
        user_has_purchased_product = Order.objects.filter(
            user=request.user,
            orderitem__product=product,
            payment_status=Order.PaymentStatusChoices.SUCCESSFUL
        ).exists()
        user_has_reviewed_product = Review.objects.filter(
            user=request.user,
            prod=product
        ).exists()

    print(user_has_reviewed_product)
    
    if request.user.is_authenticated:
        context = {
            'products': products,
            'prod_desc': prod_desc,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'user_has_purchased_product': user_has_purchased_product,
            'user_has_reviewed_product': user_has_reviewed_product,

        }
    else:
        context = {
            'products': products,
            'prod_desc': prod_desc,
            'reviews': reviews,
            'avg_rating': avg_rating,
        }
    
    return render(request, 'product/product_desc.html', context)

# def modify(request):
#     query = request.GET.get('q')
#     products = Product.objects.filter(user_id=request.user)

#     if query:
#         products = products.filter(Q(prod_name__icontains=query))
#     return render(request, 'product/modify_product.html', {'products': products, 'query': query})
#     # return render(request,'product/modify_product.html')

@login_required
@never_cache

def modify_product(request, prod_id):
    product = get_object_or_404(Product, prod_id=prod_id, user_id=request.user)
    description = ProductDescription.objects.get(prod_id=product)
    user_profile = UserProfile.objects.get(user=request.user)
    seller_request = SellerRequest.objects.get(user=request.user)
    user_addr = UserAddress.objects.get(user=request.user)

    if request.method == 'POST':
        product.prod_name = request.POST['prod_name']
        product.price = request.POST['price']
        product.stock_quantity=request.POST['quantity']
        product.sub_categ_id_id = request.POST['sub_categ_id']

        description.description = request.POST['description']
        description.instructions=request.POST['instruction']
        if 'img1' in request.FILES:
            description.img1 = request.FILES['img1']
        if 'img2' in request.FILES:
            description.img2 = request.FILES['img2']
        if 'img3' in request.FILES:
            description.img3 = request.FILES['img3']
        

        product.save()
        description.save()

        return redirect('product_list')

    subcategories = ProductSubcategory.objects.all()
  
    return render(request, 'product/modify_product.html', {'product': product, 'description': description, 'subcategories': subcategories, 'user_profile': user_profile, 'seller_request': seller_request,'user_addr' : user_addr})


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def edit_category(request, categ_id):
    # print(categ_id)
    category = get_object_or_404(ProductCategory, categ_id=categ_id)
    print(category)

    if request.method == 'POST':
        # Process the form data
        category.categ_name = request.POST['edited_categ_name']
        
        # Handle image upload
        if 'edited_categ_image' in request.FILES:
            image = request.FILES['edited_categ_image']
            file_path = f'category_images/{image.name}'
            # Save the image using Django's default storage
            default_storage.save(file_path, ContentFile(image.read()))
            category.categ_image = file_path

        category.save()
        return redirect('list_product_categories')

    return render(request, 'admin/display_cat.html', {'category': category})



# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductSubcategory, ProductCategory

def edit_subcategory_view(request, subcat_id):
    subcategory = get_object_or_404(ProductSubcategory, sub_cat_id=subcat_id)

    if request.method == 'POST':
        # Perform the update
        subcategory.sub_cat_name = request.POST.get('edited_sub_cat_name')
        subcategory.categ_id = ProductCategory.objects.get(categ_id=request.POST.get('edited_categ_id'))
        # subcategory.subcat_image = request.FILES.get('edited_subcat_image')
        if 'edited_subcat_image' in request.FILES:
            image = request.FILES['edited_subcat_image']
            file_path = f'category_images/{image.name}'
            default_storage.save(file_path, ContentFile(image.read()))
            subcategory.subcat_image = file_path
        subcategory.save()
        return redirect('list_product_subcat')  # Replace with the actual URL for your subcategory list view

    # categories = ProductCategory.objects.all()
    # return render(request, '', {'subcategory': subcategory, 'categories': categories})



def delete_category_view(request, category_id):
    category = get_object_or_404(ProductCategory, categ_id=category_id)

    if request.method == 'POST':
        # Perform the deletion
        category.delete()
        return redirect('list_product_categories')  # Replace with the actual URL for your category list view

    return render(request, 'delete_category.html', {'category': category})

def delete_subcategory(request, subcat_id):
    subcategory = get_object_or_404(ProductSubcategory, sub_cat_id=subcat_id)
    
    if request.method == 'POST':
        # Delete the subcategory
        subcategory.delete()
        return redirect('list_product_subcat')

    return render(request, 'delete_subcategory.html', {'subcategory': subcategory})

@login_required
@never_cache

def delete_product(request, prod_id):
    product = get_object_or_404(Product, prod_id=prod_id, user_id=request.user)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'product/delete_product.html', {'product': product})

@login_required
@never_cache

def add_cat(request):
    users = User.objects.all()
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
    }
    if request.method == 'POST':
        categ_name = request.POST['categ_name']
        categ_image = request.FILES['categ_image']

        # Create a new ProductCategory object and save it
        new_category = ProductCategory(categ_name=categ_name, categ_image=categ_image)
        new_category.save()

        return redirect('list_product_categories')  # Redirect to a list view of product categories
    else:
        return render(request, 'admin/add_cat.html',context)

from .models import ProductCategory

@login_required
@never_cache
def list_product_categories(request):
    users = User.objects.all()
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    categories = ProductCategory.objects.all()
    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        'categories': categories
    }
    
    return render(request, 'admin/display_cat.html', context)

    


from django.http import JsonResponse
from django.contrib.auth.models import User

def check_username(request):
    if request.method == 'GET':
        username = request.GET.get('username', '')
        user_exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': user_exists})

def check_email(request):
    if request.method == 'GET':
        email = request.GET.get('email', '')
        email_exists = User.objects.filter(email=email).exists()
        return JsonResponse({'exists': email_exists})


from django.shortcuts import render, redirect
from .models import AddCart, CartItems, Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.contrib import messages

@login_required
@never_cache

def add_to_cart(request):
    if not request.user.is_authenticated:
        return redirect('login_user') 

    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        quantity = int(request.POST.get('quantity', 1)) 

        if prod_id:
            try:
                prod = Product.objects.get(prod_id=prod_id)
            except Product.DoesNotExist:
                return HttpResponseBadRequest("Invalid product ID")

            user = request.user
            cart, created = AddCart.objects.get_or_create(user=user)

            existing_item = CartItems.objects.filter(cart=cart, prod=prod).first()
            if existing_item:
                messages.info(request, f'Already added to Cart')
            else:
                CartItems.objects.create(cart=cart, prod=prod, quantity=quantity)
                messages.info(request, f'Added to Cart')

            return redirect(request.META.get('HTTP_REFERER', 'index'))  
        else:
            return HttpResponseBadRequest("Invalid product ID")

    return render(request, 'add_to_cart.html')



from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Sum
from decimal import Decimal
from .models import AddCart, CartItems  # Import your models

@login_required
@never_cache

def cart_details(request):

    if request.user.is_authenticated:
        user = request.user
        try:
            cart = AddCart.objects.get(user=user)
            cart_items = CartItems.objects.filter(cart=cart)
        
        # Calculate total cart value and shipping cost
            total_cart_value = cart_items.aggregate(Sum('total_price'))['total_price__sum']
            if total_cart_value is None:
                total_cart_value = Decimal('0.00')  # Set a default value if total_cart_value is None
        
            shipping_cost = Decimal('50.00')  # Assuming a fixed shipping cost of $50.00
        
        # Calculate the total cost with shipping
            multiplied_value = total_cart_value + shipping_cost
        except AddCart.DoesNotExist:
            return redirect('index')  # Redirect to 'index' if the user has no AddCart entry

        return render(request, 'product/cartt.html', {'cart': cart, 'cart_items': cart_items, 'total_cart_value': total_cart_value, 'multiplied_value': multiplied_value})
    else:

      return redirect('login_user')
   

from django.http import JsonResponse
from .models import Product

def check_product_name(request):
    if request.method == 'GET':
        product_name = request.GET.get('product_name', '')
        product_exists = Product.objects.filter(prod_name=product_name).exists()
        return JsonResponse({'exists': product_exists})


from django.contrib.auth.models import User

@login_required
@never_cache

def users_list(request):
    users = User.objects.all()
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
    }
    
    return render(request, 'admin/users_list.html', context)

@login_required
@never_cache

def seller_request(request):
    users = User.objects.all()
    seller_requests = SellerRequest.objects.all()
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        'seller_requests' : seller_requests
    }
    return render(request, 'admin/seller_request.html', context)
    
   


# views.py

@login_required
@never_cache

def user_profile(request):
    # user_profile = UserProfile.objects.get(user=request.user)
    
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None

    # try:
    #     product = Product.objects.filter(user_id=request.user)
    # except Product.DoesNotExist:
    #     product = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    context = {
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        # 'product' :product
    }
    
    return render(request, 'user_profile.html', context)


from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

from .models import SellerRequest  # Import your SellerRequest model here

@login_required
@never_cache

def approve_seller(request, user_id):
    # Retrieve the seller request and user objects
    seller_request = get_object_or_404(SellerRequest, user__id=user_id)

    # Approve the seller by setting is_staff to True
    seller_request.user.is_staff = True
    seller_request.user.save()

    # You can perform additional actions here if needed, e.g., send notifications, update status, etc.

    # Return a JSON response indicating success
    # return JsonResponse({'message': 'Seller approved successfully'})
    return redirect('seller_request')

@login_required
@never_cache

def dis_approve_seller(request, user_id):
    # Retrieve the seller request and user objects
    seller_request = get_object_or_404(SellerRequest, user__id=user_id)

    # Approve the seller by setting is_staff to True
    seller_request.user.is_staff = False
    seller_request.user.save()

    # You can perform additional actions here if needed, e.g., send notifications, update status, etc.

    # Return a JSON response indicating success
    # return JsonResponse({'message': 'Seller approved successfully'})
    return redirect('seller_request')


from django.shortcuts import redirect, get_object_or_404
from .models import CartItems

@login_required
@never_cache

def remove_cart_item(request, cart_item_id):
    # Get the CartItems object by cart_item_id
    cart_item = get_object_or_404(CartItems, pk=cart_item_id)

    # Remove the CartItems object from the cart
    cart_item.delete()
    messages.success(request, f'Product removed')

    return redirect('cart_details')  # Redirect to your cart page or wherever you want



from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Use CSRF exemption for simplicity in this example; consider using CSRF protection in a real application.
def check_email_existence(request):
    email = request.POST.get('email', '')

    if User.objects.filter(email=email).exists():
        data = {'exists': True}
    else:
        data = {'exists': False}

    return JsonResponse(data)



from .models import Wishlist, Product
from django.contrib import messages

@login_required
@never_cache


def add_to_wishlist(request, prod_id):
    if not request.user.is_authenticated:
      
        return redirect('login_user')  

    product = get_object_or_404(Product, pk=prod_id)

    if Wishlist.objects.filter(user_id=request.user, prod_id=product).exists():
        messages.info(request, f'Already in your wishlist')
    else:
        Wishlist.objects.create(user_id=request.user, prod_id=product)
        messages.success(request, f'Added to wishlist')

    return redirect(request.META.get('HTTP_REFERER', 'index'))




from django.shortcuts import render
from .models import Wishlist,ProductCategory

@login_required
@never_cache

def wishlist(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # You can implement your own logic for handling unauthenticated users
        # For example, you can redirect them to a login page
        return redirect('login_user')  # Redirect to your login URL

    users = User.objects.all()

    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    

    wishlist_items = Wishlist.objects.filter(user_id=request.user)

    # subcategories = ProductSubcategory.objects.all()
    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        # 'subcategories': subcategories,
        'wishlist_items': wishlist_items
    }
    # Get the user's wishlist items

    return render(request, 'product/wishlist.html', context)


@login_required
@never_cache

def remove_wish_item(request, wish_id):
    # Get the CartItems object by cart_item_id
    wish_item = get_object_or_404(Wishlist, pk=wish_id)

    # Remove the CartItems object from the cart
    wish_item.delete()
    messages.info(request, f'Product Removed')

    return redirect('wishlist')

@login_required
@never_cache

def list_product_subcat(request):
    users = User.objects.all()
    try:
        seller_request = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        seller_request = None
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    try:
        user_addr = UserAddress.objects.get(user=request.user)
    except UserAddress.DoesNotExist:
        user_addr = None
    
    subcategories = ProductSubcategory.objects.all()
    categories = ProductCategory.objects.all()
    context = {
        'users': users,
        'user_profile': user_profile,
        'seller_request': seller_request,
        'user_addr' : user_addr,
        'subcategories': subcategories,
        'categories' :categories
    }
    
    return render(request, 'admin/display_subcat.html', context)


from django.shortcuts import render, redirect
from .models import ProductCategory, ProductSubcategory

@login_required
@never_cache

def add_subcategory(request):
    if request.method == 'POST':
        categ_id = request.POST.get('categ_id')
        sub_cat_name = request.POST.get('sub_cat_name')
        subcat_image = request.FILES.get('subcat_image')

        # Create a new ProductSubcategory instance and save it
        subcategory = ProductSubcategory(categ_id_id=categ_id, sub_cat_name=sub_cat_name, subcat_image=subcat_image)
        subcategory.save()
        return redirect('list_product_subcat')  # Redirect to a list view of subcategories

    categories = ProductCategory.objects.all()
    return render(request, 'admin/add_subcat.html', {'categories': categories})


from django.http import JsonResponse

def check_gstin_exists(request):
    gstin = request.GET.get('gstin')
    exists = SellerRequest.objects.filter(gstin=gstin).exists()
    response_data = {'exists': exists}
    return JsonResponse(response_data)

from django.http import JsonResponse
from .models import ProductSubcategory

def check_subcategory_exists(request):
    sub_cat_name = request.GET.get('sub_cat_name', None)

    if sub_cat_name:
        exists = ProductSubcategory.objects.filter(sub_cat_name=sub_cat_name).exists()
    else:
        exists = False

    data = {'exists': exists}
    return JsonResponse(data)


from django.http import JsonResponse

def check_category_exists(request):
    categ_name = request.GET.get('categ_name', None)

    if categ_name:
        exists = ProductCategory.objects.filter(categ_name=categ_name).exists()
    else:
        exists = False

    data = {'exists': exists}
    return JsonResponse(data)











from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from decimal import Decimal 

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# def homepage(request):
#     user = request.user
#     user_addr = UserAddress.objects.get(user=request.user)
#     currency = 'INR'
#     cart = AddCart.objects.get(user=user)
#     cart_items = CartItems.objects.filter(cart=cart)
#     total_cart_value = cart_items.aggregate(Sum('total_price'))['total_price__sum']
#     shipping_cost = Decimal('50.00')  # Assuming a fixed shipping cost of $50.00

#     total_cart_value = int(total_cart_value * 100)
#     shipping_cost = int(shipping_cost * 100)

#     # Calculate the total amount in paisa
#     amount = total_cart_value + shipping_cost


#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                       currency=currency,
#                                                       payment_capture='0',
#                                                       ))

#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'

#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url
#     context['total_cart_value'] = total_cart_value  # Add the total cart value as a string
#     context['shipping_cost'] = shipping_cost  # Add the shipping cost as a string
#     context['user_addr'] = user_addr

#     return render(request, 'index1.html', context=context)

# @csrf_exempt
# def paymenthandler(request):
#     # only accept POST request.
#     if request.method == "POST":
#         try:
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }

#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(params_dict)
#             if result is not None:
#                 user = request.user
#                 cart = AddCart.objects.get(user=user)
#                 cart_items = CartItems.objects.filter(cart=cart)
#                 total_cart_value = cart_items.aggregate(Sum('total_price'))['total_price__sum']
#                 shipping_cost = Decimal('50.00')  # Assuming a fixed shipping cost of $50.00

#                 total_cart_value = int(total_cart_value * 100)
#                 shipping_cost = int(shipping_cost * 100)
#                 amount = total_cart_value + shipping_cost

#                 try:
#                     # capture the payment
#                     razorpay_client.payment.capture(payment_id, amount)

#                     # render success page on successful capture of payment
#                     return render(request, 'paymentsuccess.html')
#                 except:
#                     # if there is an error while capturing payment.
#                     return render(request, 'paymentfail.html')
#             else:
#                 # if signature verification fails.
#                 return render(request, 'paymentfail.html')
#         except:
#             # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#         # if other than POST request is made.
#         return HttpResponseBadRequest()




#updated payment

from .models import AddCart, CartItems, Order, OrderItem, UserAddress

def homepage(request):
    add_cart = get_object_or_404(AddCart, user=request.user)
    cart_items = CartItems.objects.filter(cart=add_cart)
    user_add11= UserAddress.objects.get(user=request.user)


    total_price = Decimal(sum(cart_item.total_price for cart_item in cart_items))
    shipping_cost = Decimal('50.00')   
    currency = 'INR'
    amount = int((total_price+shipping_cost) * 100)
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        razorpay_order_id=razorpay_order_id,
        payment_status=Order.PaymentStatusChoices.PENDING,
    )

    for cart_item in cart_items:
        product = cart_item.prod
        price = product.price
        quantity = cart_item.quantity
        total_item_price = cart_item.total_price

        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=price,
            total_price=total_item_price,
        )

    order.save()
    

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,  # Set to 'total_price'
        'currency': currency,
        'callback_url': callback_url,
        'user_add' :user_add11
    }

    return render(request, 'index1.html', context=context)
from. models import OrderNotification_Seller

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        shipping_cost = Decimal('50.00')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        result = razorpay_client.utility.verify_payment_signature(params_dict)

        if not result:
            return render(request, 'paymentfail.html')

        try:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        except Order.DoesNotExist:
            return HttpResponseBadRequest("Order not found")

        if order.payment_status == Order.PaymentStatusChoices.SUCCESSFUL:
            
            return HttpResponse("Payment is already successful")

        if order.payment_status != Order.PaymentStatusChoices.PENDING:
            return HttpResponseBadRequest("Invalid order status")

        amount = int((order.total_price +shipping_cost)* 100)  
        razorpay_client.payment.capture(payment_id, amount)

        for order_item in order.orderitem_set.all():
            product = order_item.product
            product.stock_quantity -= order_item.quantity
            product.save()

        order.payment_id = payment_id
        order.payment_status = Order.PaymentStatusChoices.SUCCESSFUL
        order.save()

        user_address = UserAddress.objects.get(user=request.user)

        for order_item in order.orderitem_set.all():
            notification = OrderNotification_Seller.objects.create(
                prod_name=order_item.product.prod_name,
                prod_cat=order_item.product.sub_categ_id.categ_id,
                quantity=order_item.quantity,
                order=order_item,
                main_order=order,
                seller_name=order_item.product.user_id,
                noti_date=timezone.now(),  # Assuming you're using timezone from django.utils
                shipped='OR',
                district=user_address.district
            )


        add_cart = get_object_or_404(AddCart, user=request.user)
        cart_items = CartItems.objects.filter(cart=add_cart)
        cart_items.delete()

        add_cart = get_object_or_404(AddCart, user=request.user)

        cart_items = CartItems.objects.filter(cart=add_cart)
        return redirect('index')

    return HttpResponseBadRequest("Invalid request method")













from .models import Review  # Import your Review model
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

@login_required  # Ensure the user is authenticated to access this view
@never_cache

def submit_review(request):
    if request.method == 'POST':
        prod = request.POST.get('prod_id')
        prod = Product.objects.get(prod_id=prod)
        description = request.POST.get('description')
        sentiment_analyzer = SentimentIntensityAnalyzer()
        sentiment_score = sentiment_analyzer.polarity_scores(description)['compound']
        print("Sentiment Score:", sentiment_score)
        
        # Calculate the rating based on the number of stars selected
        rating = int(request.POST.get('rating', 0))

        # Create a new review associated with the product and the authenticated user
        Review.objects.create(
            user=request.user,
            rating=rating,
            description=description,
            sentiment_score=sentiment_score,
            prod=prod
        )
        
        # Redirect to a success page or the product detail page
        return redirect('index')



# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import Product

# def live_search(request):
#     if request.method == 'GET':
#         search_query = request.GET.get('query', '')
#         results = Product.objects.filter(prod_name__icontains=search_query)
#         product_data = [{'name': product.prod_name, 'description': product.productdescription.description, 'price': product.price, } for product in results]
#         return JsonResponse({'products': product_data})
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product

def live_search(request):
    if request.method == 'GET':
        search_query = request.GET.get('query', '')
        results = Product.objects.filter(prod_name__startswith=search_query)
        product_data = []

        for product in results:
            avg_rating = Review.objects.filter(prod=product).aggregate(Avg('rating'))['rating__avg'] or 0
            product_info = {
                'name': product.prod_name,
                'description': product.productdescription.description,
                'price': product.price,
                'prod_id' : product.prod_id,
                'avg_rating': avg_rating, 
                'img1_url': product.productdescription.img1.url,  # Include img1 URL
            }
            product_data.append(product_info)

        return JsonResponse({'products': product_data})



from .models import ProductCategory

# def product_request_form(request):
#     # Retrieve all categories from the database.
#     categories = ProductCategory.objects.all()

#     # Pass the categories to the template.
#     context = {
#         'categories': categories
#     }

#     return render(request, 'user/prod_request.html', context)


from django.shortcuts import render, redirect
from .models import ProductRequest
from django.contrib import messages
from .models import ProductCategory, ProductSubcategory


# def submit_request_view(request):
#     if request.method == 'POST':
#         categ_id = request.POST.get('categ_id')
#         sub_cat_name = request.POST.get('sub_cat_name')
#         subcat_image = request.FILES.get('subcat_image')

#         # Create a new ProductSubcategory instance and save it
#         subcategory = ProductRequest(requested_user=request.user,categ_id=categ_id, product_name=sub_cat_name, image=subcat_image)
#         subcategory.save()
#         return redirect('index')  # Redirect to a list view of subcategories

#     categories = ProductCategory.objects.all()
#     return render(request, 'user/prod_request.html', {'categories': categories})

from .models import ProductRequest, ProductCategory
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

@login_required
@never_cache
def submit_request_view(request):
    if request.method == 'POST':
        categ_id = request.POST.get('categ_id')
        sub_cat_name = request.POST.get('sub_cat_name')
        subcat_image = request.FILES.get('subcat_image')

        # Retrieve the ProductCategory instance based on the categ_id.
        category = get_object_or_404(ProductCategory, pk=categ_id)

        # Create a new ProductRequest instance and save it.
        product_request = ProductRequest(
            requested_user=request.user,
            categ_id=category,  # Assign the ProductCategory instance
            product_name=sub_cat_name,
            image=subcat_image
        )
        product_request.save()
        messages.success(request, f'Product request submitted')
        
        return redirect('product_requests_view')  # Redirect to a list view of subcategories

    categories = ProductCategory.objects.all()
    return render(request, 'user/prod_request.html', {'categories': categories})

        

    # Render the form if it's a GET request.



from django.shortcuts import render
from .models import ProductRequest

@login_required
@never_cache
def product_requests_view(request):
    product_requests = ProductRequest.objects.all()
    return render(request, 'admin/product_requests.html', {'product_requests': product_requests})




# from django.http import JsonResponse

# def update_cart_item(request):
#     if request.method == 'POST' and request.is_ajax():
#         cart_item_id = request.POST.get('cartItemId')
#         quantity = request.POST.get('quantity')

#         # Update the quantity in the database
#         cart_item = CartItems.objects.get(cart_item_id=cart_item_id)
#         cart_item.quantity = quantity
#         cart_item.save()

#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error'})


from django.http import JsonResponse
from django.shortcuts import render

def update_cart_quantity(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        action = request.POST.get('action')

        # Fetch the cart item from the database
        cart_item = CartItems.objects.get(cart_item_id=cart_item_id)

        # Update quantity based on the action
        
        if action == 'increment':
            if cart_item.quantity < cart_item.prod.stock_quantity:
                cart_item.quantity += 1
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1

        # Save the updated cart item
        cart_item.save()

        # Recalculate total price if needed
        cart_item.total_price = cart_item.quantity * cart_item.prod.price
        cart_item.save()

        return JsonResponse({'message': 'Quantity updated successfully'})

    return JsonResponse({'message': 'Invalid request'})



from django.shortcuts import render
from .models import ProductRequest
from django.contrib.auth.decorators import login_required

@login_required
@never_cache
def requested_products(request):
    user = request.user
    requested_products = ProductRequest.objects.filter(requested_user=user)
    return render(request, 'user/req_view.html', {'requested_products': requested_products})



# views.py
# from django.shortcuts import render
# from .models import ProductRequest

# @login_required
# @never_cache
# def product_requests_view(request):
#     product_requests = ProductRequest.objects.all()
#     return render(request, 'admin/user_req_view.html', {'product_requests': product_requests})



def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    return redirect('users_list')  # Replace 'your_user_list_view' with the actual URL name of your user list view

def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return redirect('users_list') 














# qa/views.py
from django.shortcuts import render
import torchvision
from torch import nn, optim
from torch.utils.data import DataLoader, sampler, random_split, Dataset
from torchvision.transforms import functional as FT
import pyttsx3
import math
import copy
from django.http import JsonResponse
import speech_recognition as sr





from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import os

import torch
from torchvision import datasets, models
from torchvision import transforms as T
from torch.nn import functional as F
from PIL import Image
import cv2
import albumentations as A  

import matplotlib.pyplot as plt
from pycocotools.coco import COCO
from albumentations.pytorch import ToTensorV2
from torchvision.utils import draw_bounding_boxes
import torchvision.transforms as transforms

class AquariumDetection(datasets.VisionDataset):
    def __init__(self, root, split='train', transform=None, target_transform=None, transforms=None):
        # the 3 transform parameters are reuqired for datasets.VisionDataset
        super().__init__(root, transforms, transform, target_transform)
        self.split = split #train, valid, test
        self.coco = COCO(os.path.join(root, split, "_annotations.coco.json")) # annotatiosn stored here
        self.ids = list(sorted(self.coco.imgs.keys()))
        self.ids = [id for id in self.ids if (len(self._load_target(id)) > 0)]

    def _load_image(self, id: int):
        path = self.coco.loadImgs(id)[0]['file_name']
        image = cv2.imread(os.path.join(self.root, self.split, path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    def _load_target(self, id):
        return self.coco.loadAnns(self.coco.getAnnIds(id))

    def __getitem__(self, index):
        id = self.ids[index]
        image = self._load_image(id)
        target = self._load_target(id)
        target = copy.deepcopy(self._load_target(id))

        boxes = [t['bbox'] + [t['category_id']] for t in target] # required annotation format for albumentations
        if self.transforms is not None:
            transformed = self.transforms(image=image, bboxes=boxes)

        image = transformed['image']
        boxes = transformed['bboxes']

        new_boxes = [] # convert from xywh to xyxy
        for box in boxes:
            xmin = box[0]
            xmax = xmin + box[2]
            ymin = box[1]
            ymax = ymin + box[3]
            new_boxes.append([xmin, ymin, xmax, ymax])

        boxes = torch.tensor(new_boxes, dtype=torch.float32)

        targ = {} # here is our transformed target
        targ['boxes'] = boxes
        targ['labels'] = torch.tensor([t['category_id'] for t in target], dtype=torch.int64)
        targ['image_id'] = torch.tensor([t['image_id'] for t in target])
        targ['area'] = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0]) # we have a different area
        targ['iscrowd'] = torch.tensor([t['iscrowd'] for t in target], dtype=torch.int64)
        return image.div(255), targ # scale images
    def __len__(self):
        return len(self.ids)
def get_transforms(train=False):
    if train:
        transform = A.Compose([
            A.Resize(600, 600), # our input size can be 600px
            A.HorizontalFlip(p=0.3),
            A.VerticalFlip(p=0.3),
            A.RandomBrightnessContrast(p=0.1),
            A.ColorJitter(p=0.1),
            ToTensorV2()
        ], bbox_params=A.BboxParams(format='coco'))
    else:
        transform = A.Compose([
            A.Resize(600, 600), # our input size can be 600px
            ToTensorV2()
        ], bbox_params=A.BboxParams(format='coco'))
    return transform




def average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]



# Get the absolute path of the directory containing this script
current_directory = os.path.dirname(os.path.realpath(__file__))

# Specify the absolute path to 'demo1.csv'
file_path = os.path.join(current_directory, 'demo1.csv')
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Load fish data from a CSV file
fish_data = pd.read_csv(file_path)

# Initialize the KNN model
nn_model = NearestNeighbors(n_neighbors=5, metric='cosine', algorithm='brute')
nn_model.fit(fish_data[['Aggression Level', 'Social Behavior', 'Territoriality', 'Schooling Behavior', 'Predatory', 'Size', 'Compatibility']])


def homeee(request, prod_id):
    product = get_object_or_404(Product, pk=prod_id)
    product_description = get_object_or_404(ProductDescription, prod_id=product)
    if request.method == 'POST':
        user_question = request.POST.get('description')
        

        # Make predictions here
        # context = 'Betta fish prefer their water’s pH to be slightly acidic. They do best in the pH range of 6.5 to 7.5 (7 is neutral). Some tap water and spring water may be significantly higher than 7.5 which means you should always test your water before adding it to your betta’s tank. Consider purchasing a pH kit to keep it in a healthy range if necessary. Also consider adding aquarium salt to your aquarium’s water to reduce stress and swelling, and to promote healthy fins. A systematic maintenance schedule must be adhered to. Tanks under 3 gallons will need more frequent and complete water changes to avoid dangerous levels of ammonia. It can be done, it’s just more work. Non-filtered tanks require 1-2 water cycles at around 25% and a full 100% water change each week (depending on water quality). A 5-gallon filtered tank will only need 1-2 water cycles per week at around 25% of total volume and a 100% water change once per month depending on water quality. Keep a pH kit in your supplies to test your tank’s water. Don’t combine your betta with fish that are notorious for fin nippers. Smaller tanks and those that are unfiltered are more work in the long-run because of how rapidly the water’s quality can decline. Cleaning your tank and its decorations every week is very important for your betta fish’s health. Only use approved aquarium decorations and materials that are safe for fish. Use a magnetic or algae cleaning wand for regular algae removal while the tank is filled. Filters and their media should be cleaned by rinsing them in existing tank water to preserve healthy bacteria. Other components should be cleaned and disinfected. Never clean a tank or its components with soap! It’s very tough to remove all the soap and it can poison your betta once the tank is refilled. Remember, adding live plants can also help reduce ammonia levels in the water naturally. Water cycling (removing some and adding new) and changes (complete volume replacement) are necessary for filtered tanks too but are more frequent and important in non-filtered habitats. If you’re only cycling the water, don’t remove your betta. Unnecessary removal can lead to potential stress and injury. Only remove your betta during 100% water changes. Betta fish get used to their ecosystem and don’t like abrupt changes to it. Because of this, you should cycle more than you do a complete change. Removing too much of the existing water in the tank and then adding new can cause your fish to go into shock. This may be due to changes in water parameters or temperature. Always acclimate your betta fish when re-introducing them to their tank after a complete water change.'
        context = product_description.description


        input_texts = [
        "similar fish",
        "recommend fishes similar to this fish",
        "identify the fishes from image" 
        ]

        # Get another word from the user
        # user_input = input("Enter another word or phrase: ")
        input_texts.append(user_question)

        tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-large")
        model = AutoModel.from_pretrained("thenlper/gte-large")

        # Tokenize the input texts
        batch_dict = tokenizer(input_texts, max_length=512, padding=True, truncation=True, return_tensors='pt')

        outputs = model(**batch_dict)
        embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])

        # (Optionally) normalize embeddings
        embeddings = F.normalize(embeddings, p=2, dim=1)

        # Calculate similarity scores
        similar_threshold = 95
        not_similar_threshold = 95
        tank_threshold = 95

        # ... (previous code)

        # Calculate similarity scores
        max_similarity = -1
        max_similarity_index = -1
        threshold = 90

        for i, text in enumerate(input_texts[:-1]):
            scores = (embeddings[i] @ embeddings[-1].T) * 100
            print(f"Similarity between '{text}' and '{user_question}': {scores.item()}")

            if scores.item() > max_similarity and scores.item() > threshold:
                max_similarity = scores.item()
                max_similarity_index = i

        if max_similarity_index == 0 or max_similarity_index == 1:
            input_fish_name = product.fish_name.fish_name
            input_fish_features = fish_data.loc[fish_data['Species'] == input_fish_name, ['Aggression Level', 'Social Behavior', 'Territoriality', 'Schooling Behavior', 'Predatory', 'Size', 'Compatibility']].values[0]
            
            # Find similar fish using KNN
            _, neighbor_indices = nn_model.kneighbors(input_fish_features.reshape(1, -1))
            similar_fish_indices = neighbor_indices[0][1:]
            similar_fish = fish_data.iloc[similar_fish_indices]

            # Convert similar fish data to JSON format
            similar_fish_json = similar_fish['Species'].tolist()

            # Print or use the similar fish data as needed
            print(f"Fish similar to {input_fish_name} ")
            print(similar_fish[['Species']])

            # similar_fish_text = ", ".join(similar_fish_json)
            # engine = pyttsx3.init()
            # engine.say(f"Fish similar to {input_fish_name} are: {similar_fish_text}")
            # engine.runAndWait()

            return JsonResponse({'similar_fish': similar_fish_json, 'input_fish_name': input_fish_name})
    
        elif max_similarity_index == 2:
            
            if 'upload-image' in request.FILES:
                image = request.FILES['upload-image']
                print(image)
                print(os.getcwd())
                device = torch.device("cpu")  # use GPU to train
                model = torch.load('./outt')
                model.eval()
                torch.cuda.empty_cache()
                dataset_path = "./Aquarium Combined/"
                coco = COCO(os.path.join(dataset_path, "train", "_annotations.coco.json"))
                categories = coco.cats
                n_classes = len(categories.keys())
                classes = [i[1]['name'] for i in categories.items()]

                img = Image.open(image)
                transform = transforms.Compose([transforms.ToTensor()])
                img_tensor = transform(img)

                img_int = (img_tensor * 255).to(torch.uint8)

                fig, ax = plt.subplots(figsize=(14, 10))

                with torch.no_grad():
                    prediction = model([img_tensor])
                    pred = prediction[0]
                    print(pred)

                    # Assuming draw_bounding_boxes returns an image
                    img_with_boxes = draw_bounding_boxes(
                        img_int,
                        pred['boxes'][pred['scores'] > 0.8],
                        [classes[i] for i in pred['labels'][pred['scores'] > 0.8].tolist()],
                        width=4
                    ).permute(1, 2, 0)

                    # Set the extent to match the image size
                    extent = [0, img_int.shape[2], img_int.shape[1], 0]

                    ax.imshow(img_with_boxes, extent=extent)
                    ax.axis('off')  # Turn off axis if not needed

                    temp_file_path = "static/ml/temp_image.png"
                    fig.savefig(temp_file_path, bbox_inches='tight', pad_inches=0)
                    labels = [classes[i] for i in pred['labels'][pred['scores'] > 0.8].tolist()]
                    print(labels)

                print(temp_file_path)
                return JsonResponse({'image_predicted_answer': labels, 'temp_image_path': temp_file_path, 'static_path': '/static/'})
            else:
                return JsonResponse({'image_predicted_answer': 'No image file provided'})
        elif max_similarity_index == -1:
            model_name = "deepset/roberta-base-squad2"
            model = AutoModelForQuestionAnswering.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

            res = nlp({'question': user_question, 'context': context})
            score = res['score']
            # predicted_answer = res['answer']
            if score > 0.03:
                predicted_answer = res['answer']
            else:
                predicted_answer = "OOPS! Can't find the answer"

            # engine = pyttsx3.init()
            # engine.say("The predicted answer is: " + predicted_answer)
            # engine.runAndWait()
            

            return JsonResponse({'predicted_answer': predicted_answer})
        else:
            print(f"No index with similarity score greater than the threshold :{max_similarity_index}")

















        # model_name = "deepset/roberta-base-squad2"
        # model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        # tokenizer = AutoTokenizer.from_pretrained(model_name)
        # nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

        # res = nlp({'question': user_question, 'context': context})
        # predicted_answer = res['answer']


        # if any(keyword in user_question.lower() for keyword in ['similar fish', 'similar fishes', 'fish similar', 'fish similar to this fish']):
        #     # Assume 'input_fish_name' is extracted from the user's question (modify as needed)
        #     input_fish_name = product.fish_name.fish_name
        #     input_fish_features = fish_data.loc[fish_data['Species'] == input_fish_name, ['Aggression Level', 'Social Behavior', 'Territoriality', 'Schooling Behavior', 'Predatory', 'Size', 'Compatibility']].values[0]
            
        #     # Find similar fish using KNN
        #     _, neighbor_indices = nn_model.kneighbors(input_fish_features.reshape(1, -1))
        #     similar_fish_indices = neighbor_indices[0][1:]
        #     similar_fish = fish_data.iloc[similar_fish_indices]

        #     # Convert similar fish data to JSON format
        #     similar_fish_json = similar_fish['Species'].tolist()

        #     # Print or use the similar fish data as needed
        #     print(f"Fish similar to {input_fish_name} ")
        #     print(similar_fish[['Species']])

        #     similar_fish_text = ", ".join(similar_fish_json)
        #     engine = pyttsx3.init()
        #     engine.say(f"Fish similar to {input_fish_name} are: {similar_fish_text}")
        #     engine.runAndWait()

        #     return JsonResponse({'similar_fish': similar_fish_json})
        
        # else:
        #     # Speak the predicted result
        #     engine = pyttsx3.init()
        #     engine.say("The predicted answer is: " + predicted_answer)
        #     engine.runAndWait()

           #     return JsonResponse({'predicted_answer': predicted_answer})


def imagee(request):
    if request.method == "POST":
        image = request.FILES['upload-image']
        print(image)
        print(os.getcwd())
        device = torch.device("cpu") # use GPU to train
        model = torch.load('./outt')
        model.eval()
        torch.cuda.empty_cache()
        dataset_path = "./Aquarium Combined/"
        coco = COCO(os.path.join(dataset_path, "train", "_annotations.coco.json"))
        categories = coco.cats
        n_classes = len(categories.keys())
        classes = [i[1]['name'] for i in categories.items()]

        # test_dataset = AquariumDetection(root=dataset_path, split="test", transforms=get_transforms(False))
        # img, _ = test_dataset[9]
        # img_int = torch.tensor(img*255, dtype=torch.uint8)
        img = Image.open(image)
        transform = transforms.Compose([transforms.ToTensor()])
        img_tensor = transform(img)

        img_int = (img_tensor * 255).to(torch.uint8)


        # img_int = torch.tensor(img * 255, dtype=torch.uint8)

        fig = plt.figure(figsize=(14, 10))
        with torch.no_grad():
            # prediction = model([img.to(device)])
            prediction = model([img_tensor])
            pred = prediction[0]
            print(pred)
            plt.imshow(draw_bounding_boxes(img_int,
                                    pred['boxes'][pred['scores'] > 0.8],
                                    [classes[i] for i in pred['labels'][pred['scores'] > 0.8].tolist()], width=4
                                    ).permute(1, 2, 0))
            temp_file_path = "static/ml/temp_image9.png"
            fig.savefig(temp_file_path)
    return redirect('index')
 



# def filter_products(request):
#     price_range = request.GET.getlist('price')
#     ratings = request.GET.getlist('rating')

#     # Filter products based on selected price range and ratings
#     filtered_products = Product.objects.filter(
#         sub_categ_id=subcat_id,
#         price__range=price_range,
#         review__rating__in=ratings
#     ).distinct()

#     return render(request, 'product/filtered_products.html', {'filtered_products': filtered_products})
from django.http import JsonResponse

import json

def filter_products(request):
    price_range = json.loads(request.GET.get('price', '[]'))
    ratings = request.GET.getlist('rating')

    # Filter products based on selected price range and ratings
    filtered_products = Product.objects.filter(
        price__range=price_range,
        review__rating__in=ratings
    ).distinct()

    # Convert filtered products to a list of dictionaries
    products_list = [
        {'prod_name': product.prod_name, 'price': product.price}
        for product in filtered_products
    ]

    return JsonResponse({'filtered_products': products_list})

    
    
    
    
    return render(request, '')


from .models import Event
@login_required
@never_cache
def events(request):
    events = Event.objects.all()
    return render(request, 'events/events.html', {'events': events})

@login_required
@never_cache
def all_events(request):
    events = Event.objects.all()
    return render(request, 'events/all_events.html', {'events': events})



# views.py
# views.py
# views.py

from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.utils.dateparse import parse_date
from django.utils import timezone  # Import timezone
from .models import Event

@login_required
@never_cache
def add_event(request):
    if request.method == 'POST':
        # Process the form submission
        name = request.POST.get('name')
        event_img = request.FILES.get('event_img')
        date_str = request.POST.get('date')
        description = request.POST.get('description')
        mode = request.POST.get('mode')
        # duration = request.POST.get('duration')  # Get duration as a string
        booking_link = request.POST.get('booking_link')

        # Convert date string to datetime object
        try:
            date = parse_date(date_str)
        except ValueError:
            # Handle invalid date format
            # You can add your own error handling logic here
            return render(request, 'events/add_event.html', {'error_message': 'Invalid date format'})

        # Convert duration string to timedelta object
        # try:
        #     duration = timezone.timedelta(seconds=int(duration_str))
        # except ValueError:
        #     # Handle invalid duration format
        #     # You can add your own error handling logic here
        #     return render(request, 'events/add_event.html', {'error_message': 'Invalid duration format'})

        Event.objects.create(
            name=name,
            event_img=event_img,
            date=date,
            description=description,
            mode=mode,
            # duration=duration,
            booking_link=booking_link,
        )

        # return redirect('list_product_subcat')  # Redirect to the desired URL after adding the event

    return render(request, 'events/add_event.html')

from datetime import timedelta

@login_required
@never_cache
def edit_event(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)

    if request.method == 'POST':
        # Perform the update
        event.name = request.POST.get('edited_event_name')
        event.date = request.POST.get('date')
        event.description = request.POST.get('description')
        event.mode=request.POST.get('edited_event_mode')
        # duration_seconds = int(request.POST.get('edited_event_duration'))
        event.duration = request.POST.get('edited_event_duration')
        # event.mode=request.POST.get('edited_booking_link')
        event.booking_link=request.POST.get('edited_booking_link')

        # subcategory.categ_id = ProductCategory.objects.get(categ_id=request.POST.get('edited_categ_id'))
        # # subcategory.subcat_image = request.FILES.get('edited_subcat_image')
        if 'edited_event_image' in request.FILES:
            image = request.FILES['edited_event_image']
            file_path = f'events/{image.name}'
            default_storage.save(file_path, ContentFile(image.read()))
            event.event_img = file_path
        event.save()
        return redirect('all_events') 

@login_required
@never_cache
def delete_event(request, event_id):
    event=get_object_or_404(Event, event_id=event_id)
    print(event)
    event.delete()
    return redirect('all_events')



from django.db.models import Sum



# def calculate_product_sentiment_score():
#     # Use annotate to add a new field to each product with the sum of sentiment scores for its reviews
#     products_with_sentiment_sum = Product.objects.annotate(sentiment_sum=Sum('review__sentiment_score'))

#     for product in products_with_sentiment_sum:
#         print(f"Product {product.prod_name} Sentiment Sum: {product.sentiment_sum}")

# # Call the function to calculate and print the sum of sentiment scores for each product
# calculate_product_sentiment_score()


def top_products(request):
    # Use annotate to add a new field to each product with the sum of sentiment scores for its reviews
    products_with_sentiment_sum = Product.objects.annotate(sentiment_sum=Sum('review__sentiment_score')).order_by('-sentiment_sum')[:5]

    context = {'products_with_sentiment_sum': products_with_sentiment_sum}
    return render(request, 'Review/top_products.html', context)


from .models import Subscription_details
@login_required
@never_cache
def subscription(request):
    subscription=Subscription_details.objects.all()
    # subscriptionn=Subscription.objects.filter(user=request.user)
    latest_subscription = Subscription.objects.filter(user=request.user).order_by('-order_date').first()
    # print(latest_subscription.expiration_date)
    a=timezone.now()
    # if a < latest_subscription.expiration_date:
    #    latest_subscription.status = False
    #    latest_subscription.save()
 

    print("now:",a)
    print("exp:")
    context = {
        'subscription':subscription,
        'latest_subscription': latest_subscription,
        'is_subscribed': latest_subscription.status if latest_subscription else False,
        'a':a
    }

    return render(request,'subscription/sub.html', context)




from .models import Subscription
@login_required
@never_cache
def sub_pay(request):
    user_add11= UserAddress.objects.get(user=request.user)


    total_price = float(request.GET.get("amount")) 
    currency = 'INR'
    amount = int((total_price) * 100)
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandlerr/'

    subscription = Subscription.objects.create(
        user=request.user,
        total_price=total_price,
        razorpay_order_id=razorpay_order_id,
        payment_status=Subscription.PaymentStatusChoices.PENDING,
    )

  
    subscription.save()
    

    context = {
        'total_price': total_price,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,  # Set to 'total_price'
        'currency': currency,
        'callback_url': callback_url,
        'user_add' :user_add11
    }

    return render(request, 'pay_sub.html', context=context)

@csrf_exempt
@login_required
@never_cache
def paymenthandlerr(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        result = razorpay_client.utility.verify_payment_signature(params_dict)

        if not result:
            return render(request, 'paymentfail.html')

        try:
            subscription = Subscription.objects.get(razorpay_order_id=razorpay_order_id)
        except Subscription.DoesNotExist:
            return HttpResponseBadRequest("Order not found")

        if subscription.payment_status == Subscription.PaymentStatusChoices.SUCCESSFUL:
            
            return HttpResponse("Payment is already successful")

        if subscription.payment_status != Subscription.PaymentStatusChoices.PENDING:
            return HttpResponseBadRequest("Invalid order status")

        amount = int((subscription.total_price)* 100)  
        razorpay_client.payment.capture(payment_id, amount)
        subscription.payment_id = payment_id
        subscription.payment_status = Subscription.PaymentStatusChoices.SUCCESSFUL
        subscription.save()
        return redirect('index')

    return HttpResponseBadRequest("Invalid request method")


from .models import CommunityPost


from datetime import datetime, timedelta
from django.db.models import Count

def blog(request):
    # Calculate the date 30 days ago from today
    thirty_days_ago = datetime.now() - timedelta(days=30)

    # Filter posts created within the last 30 days
    recent_posts = CommunityPost.objects.filter(date_created__gte=thirty_days_ago)
    for i in recent_posts:
        print({i.heading},{i.likes})

    # Annotate each post with the number of likes and order by likes descending
    # recent_posts = recent_posts.annotate(num_likes=Count('likes')).order_by('-num_likes')[:6]
    recent_posts = CommunityPost.objects.filter(date_created__gte=thirty_days_ago).order_by('-likes')[:6]
    for post in recent_posts:
        print(f"Post: {post.heading}, Likes: {post.likes}")


    context = {
        'latest_popular_posts': recent_posts
    }
    return render(request, 'blog/index.html', context)



from django.shortcuts import render, redirect

@login_required
@never_cache
def add_community_post(request):
    if request.method == 'POST':
        heading = request.POST.get('heading')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        if heading and description:  # Basic validation, you might want to add more
            if request.user.is_authenticated:  # Check if user is logged in
                CommunityPost.objects.create(user=request.user, heading=heading, description=description, image=image)
                return redirect('user_posts')  # Redirect to home page after successful submission
            else:
                return redirect('login')  # Redirect to login page if user is not logged in
    return render(request, 'blog/add_community_post.html')


from .models import CommunityPost
@login_required
@never_cache
def user_posts(request):
    if request.user.is_authenticated:
        user_posts = CommunityPost.objects.filter(user=request.user)
        return render(request, 'blog/user_posts.html', {'user_posts': user_posts})
    else:
        # Redirect to login page if user is not authenticated
        return redirect('login')



from .models import CommunityPost, PostLikes

from django.http import JsonResponse
@login_required
@never_cache
def like_post(request, post_id):
    print(post_id)
    post = CommunityPost.objects.get(pk=post_id)
    liked_user = request.user
    if not PostLikes.objects.filter(post_id=post, liked_user=liked_user).exists():
        post_like = PostLikes(post_id=post, liked_user=liked_user)
        post_like.save()
        post.likes += 1
        post.save()
    return JsonResponse({'likes': post.likes})


@login_required
@never_cache
def get_post(request, post_id):
    post_si = get_object_or_404(CommunityPost, post_id=post_id)
    return render(request, 'post_detail.html', {'post': post})


@login_required
@never_cache
def admin_show_products(request):
    show_pdts=Product.objects.all()
    return render(request, 'admin/show_products.html',{'show_pdts': show_pdts})


from .models import Order
@login_required
@never_cache
def my_orders(request):
    
    show_orders = Order.objects.filter(user=request.user, payment_status=Order.PaymentStatusChoices.SUCCESSFUL)
    for i in show_orders:
        print(i)
    return render(request, 'Orders/show_orders.html',{'show_orders': show_orders})





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChatMessage
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render
from .models import UserProfile

def community(request):
    chat_messages = ChatMessage.objects.select_related('user__userprofile').all()
    # users_with_avatars = User.objects.filter(userprofile_profile_image_isnull=False)
    return render(request, 'Community/community.html', {'chat_messages': chat_messages})


@login_required
def send_message(request):
    if request.method == 'POST':
        user = request.user
        message = request.POST.get('message', '')
        if message:
            chat_message = ChatMessage.objects.create(user=user, message=message)
            channel_layer = get_channel_layer()
            try:
                async_to_sync(channel_layer.group_send)(
                    'chat_group',
                    {
                        'type': 'chat.message',
                        'message': chat_message.message,
                        'username': user.username,
                    }
                )
            except Exception as e:
                print(f"Error sending message: {e}")
            messages.success(request, 'Message sent successfully!')
            return redirect('community')
        else:
            messages.error(request, 'Invalid message. Please enter a non-empty message.')
            
    return redirect('community')



from django.shortcuts import render
from .models import Product

from django.shortcuts import render
from .models import Product

from django.shortcuts import render
from .models import Product

# def filter_products(request):
#     if request.method == 'POST':
#         price_ranges = {
#             '0-100': (0, 100),
#             '101-200': (101, 200),
#             '201-500': (201, 500)
#         }
#         min_value = request.POST.get('min-value')
#         max_value = request.POST.get('max-value')


#         # Do something with the min and max values
#         print("Minimum Value:", min_value)
#         print("Maximum Value:", max_value)

#         selected_price_ranges = request.POST.getlist('price_range')
#         print(selected_price_ranges)

#         selected_ratings = request.POST.getlist('rating')
#         subcat_id = request.POST.get('subcat_id')
        
#         # Prepare price range filters
#         price_filters = []
#         for price_range in selected_price_ranges:
#             price_range_tuple = price_ranges.get(price_range)
#             if price_range_tuple:
#                 price_filters.append(price_range_tuple)
        
#         # Combine price range filters if multiple are selected
#         combined_price_filter = None
#         for price_filter in price_filters:
#             if combined_price_filter is None:
#                 combined_price_filter = price_filter
#             else:
#                 combined_price_filter = (
#                     min(combined_price_filter[0], price_filter[0]),
#                     max(combined_price_filter[1], price_filter[1])
#                 )
        
#         # Query products based on selected filters
#         filtered_products = Product.objects.filter(
#             sub_categ_id=subcat_id,
#             # rating__in=selected_ratings
#         )
        
#         # Apply combined price range filter
#         if combined_price_filter:
#             filtered_products = filtered_products.filter(price__range=combined_price_filter)
        

#         for i in filtered_products:
#             print(i)
#         # Render the filtered products in your template
#         return redirect('index')
#         # return render(request, 'filtered_products.html', {'products': filtered_products})
#     else:
#         # Handle GET request or render initial form
#         pass
import math
def filter_products(request):
    if request.method == 'POST':
        min_value = request.POST.get('min-value')
        max_value = request.POST.get('max-value')
        selected_ratings = request.POST.getlist('rating')
        selected_ratings_as_int = [int(rating) for rating in selected_ratings]
        print("selec",selected_ratings_as_int)

        print("Minimum Value:", min_value)
        print("Maximum Value:", max_value)

        subcat_id = request.POST.get('subcat_id')
        matching_products = []
        
        filtered_products = Product.objects.filter(
            sub_categ_id=subcat_id,
            price__gte=min_value,  
            price__lte=max_value   
        )
        matching_products = []
        for product in filtered_products:
            avg_rating = Review.objects.filter(prod=product).aggregate(Avg('rating'))['rating__avg'] or 0
            print("avggg:", product.prod_name, avg_rating)
            print("selec",selected_ratings)
            a=math.ceil(avg_rating)
            print("ceil",a)
            # print(a)

            # if a in selected_ratings_as_int :
            #     print("hellosefff")
            if a in selected_ratings_as_int:
                matching_products.append(product)
                print("avg_rating:", product.prod_name, avg_rating)
                # b=math.ceil(avg_rating)
                # print("b",b)
            if not selected_ratings_as_int:
                matching_products.append(product)
                # print("avg_rating:", product.prod_name, avg_rating)

        # for i in matching_products:
        #     print(i,i.price,b)  

        serialized_products = [{'name': product.prod_name, 'price': product.price, 'img':product.productdescription.img1.url, 'avg_rating':avg_rating,'prod_id':product.prod_id} for product in matching_products]

        # Return JSON response
        return JsonResponse({'products': serialized_products})
    else:
        pass




# # react
# from django.contrib.auth import authenticate, login
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt 
# def user_loginnn(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         email = data.get('email')
#         password = data.get('password')
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)

# from .models import ProductCategory
# def show_user(request):
#     # Retrieve all user profiles from the database
#     user_profiles = ProductCategory.objects.all()
    
#     # Convert user profiles to JSON format
#     user_profiles_json = [
#         {
#             'id': profile.categ_id,
#             'name': profile.categ_name,
#             'image': request.build_absolute_uri(profile.categ_image.url) if profile.categ_image else None,
#             'craeted_at': profile.created_at,

#         }
#         for profile in user_profiles
#     ]
    
#     # Return the user profiles as a JSON response
#     return JsonResponse(user_profiles_json, safe=False)


from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

class GeneratePDF(View):
    template_name = 'invoice_template.html'

    def get(self, request, *args, **kwargs):
        # Fetch order details from the database based on the order_id
        order_id = kwargs['order_id']
        order = Order.objects.get(id=order_id)

        # Render the template
        template = get_template(self.template_name)
        context = {'order': order}
        html = template.render(context)

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=invoice_{order_id}.pdf'

        # Generate PDF using ReportLab
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response

from .models import OrderNotification_Seller
def requested_orders(request):
    orders=OrderNotification_Seller.objects.filter(seller_name=request.user)
    return render(request,'Orders/requested_orders.html',{'orders':orders})


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import OrderNotification_Seller

@require_POST
def update_shipped(request, notification_id):
    notification = OrderNotification_Seller.objects.get(pk=notification_id)
    
    if request.method == 'POST':
        # Perform the deletion
        notification.shipped = 'DL' 
        notification.save()
        return redirect('requested_orders')  # Replace with the actual URL for your category list view


def order_status_hub(request):
    user=request.user
    orders=OrderNotification_Seller.objects.filter(hub=user.useraddress.district)
    # for a in orders:
    #     print(a.)
    return render(request,'Orders/order_status_hub.html',{'orders':orders})


@require_POST
def update_shipped1(request, notification_id):
    notification = OrderNotification_Seller.objects.get(pk=notification_id)
    
    if request.method == 'POST':
        # Perform the deletion
        notification.shipped = 'SU' 
        notification.save()
        return redirect('order_status_hub')  # Replace with the actual URL for your category list view


@require_POST
def update_tank(request, notification_id):
    notification = OrderNotification_Seller.objects.get(pk=notification_id)
    
    if request.method == 'POST':
        # Perform the deletion
        notification.stored_tank = request.POST.get('tank_id') 
        notification.save()
        return redirect('order_status_hub')  # Replace with the actual URL for your category list view


def artemia(request):
    return render(request,"Guide/guide.html")