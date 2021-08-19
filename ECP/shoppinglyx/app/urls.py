from django.urls import path,include
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MySetPasswordForm,MyPasswordRestForm

urlpatterns = [
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.productdetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart1/', views.Remove_cart),
    path('search/', views.search, name='search'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('update/<id>', views.address_update, name='update'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/',auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',
                form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'), name='changepassword'),

    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),
         name='passwordchangedone'),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',
                                                                form_class=MyPasswordRestForm),name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),
                       name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
                        template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),
                       name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),
                       name='password_reset_complete'),



    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),

    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),

    path('top/', views.topwear, name='top'),
    path('top/<slug:data>', views.topwear, name='topdata'),

    path('bottom/', views.bottomwear, name='bottom'),
    path('bottom/<slug:data>', views.bottomwear, name='bottomdata'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),

    path('api/', include('app.Api.urls')),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
