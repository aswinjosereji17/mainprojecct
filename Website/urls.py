from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import GeneratePDF



urlpatterns = [
    path('',views.index, name='index'),
    path('login_user',views.login_user,name='login_user'),
    path('register/',views.register,name='register'),
    path('seller_register',views.seller_register,name='seller_register'),
    path('loggout',views.loggout,name='loggout'),
    path('user_profile_view', views.user_profile_view, name='user_profile_view'),
    
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    # path('add_product/', views.add_product, name='add_product'), 
    # path('get_subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),

    path('product_list', views.product_list, name='product_list'),
    path('add_product', views.add_product, name='add_product'),
    path('subcategories/<int:categ_id>/', views.subcategories_view, name='subcategories'),
    path('subcategory_products/<int:subcat_id>/', views.subcategory_products_view, name='subcategory_products'),
    path('prod_desc/<int:prod_id>/', views.prod_desc, name='prod_desc'),
    path('modify-product/<int:prod_id>/', views.modify_product, name='modify_product'),
    path('delete-product/<int:prod_id>/', views.delete_product, name='delete_product'),

    # path('modify-product', views.modify_product, name='modify_product'),
    path('add_cat', views.add_cat, name='add_cat'),
    path('product_categories/', views.list_product_categories, name='list_product_categories'),
    path('list_product_subcat/', views.list_product_subcat, name='list_product_subcat'),
    path('add_subcategory/', views.add_subcategory, name='add_subcategory'),

    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),




    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart_details', views.cart_details, name='cart_details'),
    path('check_product_name/', views.check_product_name, name='check_product_name'),

    path('users_list/', views.users_list, name='users_list'),
    path('seller_request/', views.seller_request, name='seller_request'),

    path('check-category-exists/', views.check_category_exists, name='check-category-exists'),    path('user_profile/', views.user_profile, name='user_profile'),
    path('approve-seller/<int:user_id>/', views.approve_seller, name='approve_seller'),
    path('dis_approve-seller/<int:user_id>/', views.dis_approve_seller, name='dis_approve_seller'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('add_to_wishlist/<int:prod_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('check_gstin_exists/', views.check_gstin_exists, name='check-gstin-exists'),
    path('check-subcategory-exists/', views.check_subcategory_exists, name='check-subcategory-exists'),
    path('remove_wish_item/<int:wish_id>/', views.remove_wish_item, name='remove_wish_item'),



    path('homepage', views.homepage, name='homepage'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),


    path('submit_review/', views.submit_review, name='submit_review'),

    path('live_search/', views.live_search, name='live_search'),

    path('filter-products/', views.filter_products, name='filter_products'),

    # path('product_request_form/', views.product_request_form, name='product_request_form'),
    path('submit_request_view/', views.submit_request_view, name='submit_request_view'),
    path('product_requests_view/', views.product_requests_view, name='product_requests_view'),


    # path('update_cart_item/', views.update_cart_item, name='update_cart_item'),

    path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),


    path('requested_products/', views.requested_products, name='requested_products'),
    path('homeee/<int:prod_id>/', views.homeee, name='homeee'),
    path('ml', views.imagee,name='ml'),
    path('edit_category/<int:categ_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category_view, name='delete_category'),
    path('edit_subcategory/<int:subcat_id>/', views.edit_subcategory_view, name='edit_subcategory'),
    path('delete_subcategory/<int:subcat_id>/', views.delete_subcategory, name='delete_subcategory'),


    # path('product_requests_view/', views.product_requests_view, name='product_requests_view'),


    path('events/', views.events, name='events'),
    path('add_event/', views.add_event, name='add_event'),
    path('all_events/', views.all_events, name='all_events'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),

    # path('display_top_products/', views.display_top_products, name='display_top_products'),

    path('top-products/', views.top_products, name='top_products'),

    path('subscription/',views.subscription, name='subscription'),




    path('sub_pay', views.sub_pay, name='sub_pay'),
    path('paymenthandlerr/', views.paymenthandlerr, name='paymenthandlerr'),
    path('blog', views.blog, name='blog'),
    path('add/', views.add_community_post, name='add_community_post'),
    path('user_posts/', views.user_posts, name='user_posts'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('get_post/<int:post_id>/', views.get_post, name='get_post'),

    path('admin_show_products/', views.admin_show_products, name='admin_show_products'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('community/', views.community, name='community'),
    path('send_message/', views.send_message, name='send_message'),
    path('filter_products/', views.filter_products, name='filter_products'),



    # path('user_loginnn/', views.user_loginnn, name='user_loginnn'),
    # path('show_user/', views.show_user, name='show_user'),

    path('generate-pdf/<int:order_id>/', GeneratePDF.as_view(), name='generate_pdf'),
    path('requested_orders/', views.requested_orders, name='requested_orders'),
    path('update_shipped/<int:notification_id>/', views.update_shipped, name='update_shipped'),
    path('update_shipped1/<int:notification_id>/', views.update_shipped1, name='update_shipped1'),
    path('update_tank/<int:notification_id>/', views.update_tank, name='update_tank'),


    path('order_status_hub/', views.order_status_hub, name='order_status_hub'),
    path('artemia/',views.artemia,name='artemia')

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
 