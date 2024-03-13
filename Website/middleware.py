# middleware.py

from Website.models import ProductCategory, ProductSubcategory

class CommonDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add common data to request
        request.prod_cat = ProductCategory.objects.all()
        request.prod_subcat = ProductSubcategory.objects.all()

        response = self.get_response(request)
        return response
