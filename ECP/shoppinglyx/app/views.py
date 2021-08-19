from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from . models import Product,Cart,Customer,OrderPlaced
from .forms import CustomRegistrationForm,CustomerProfileForm,CustomerupdateForm
from django.contrib import messages
from  django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
  def get(self,request):
      totalitem=0
      mobiles=Product.objects.filter(category='m')
      laptops=Product.objects.filter(category='L')
      topwear=Product.objects.filter(category='TW')
      bottomwear = Product.objects.filter(category='BW')
      if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))


      return render(request,'app/home.html',{'totalitem':totalitem, 'mobiles':mobiles,'laptops':laptops,'topwear':topwear,'bottomwear':bottomwear})


class productdetailView(View):
    def get(self,request,pk):
        totalitem=0
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

            item_already_in_cart=Cart.objects.filter(Q(product=product.id) &Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'totalitem':totalitem,'product':product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    cart=Cart(user=user,product=product)
    cart.save()

    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amt=70.0
        totalamt=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user ]
        if cart_product:
            for p in cart_product:
                tempamout=(p.quantity * p.product.discounted_price)
                amount+=tempamout
                totalamt=amount + shipping_amt
            return render(request, 'app/addtocart.html',{'cart':cart,'amount':amount,'totalamt':totalamt,'totalitem':totalitem})

        else:
            return render(request, 'app/emptycart.html',{'totalitem':totalitem})

@login_required
def plus_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amt = 70.0
        totalamt = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamout = (p.quantity * p.product.discounted_price)
                amount += tempamout
                totalamt = amount + shipping_amt
            data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamt':totalamt
            }
            return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amt = 70.0
        totalamt = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamout = (p.quantity * p.product.discounted_price)
                amount += tempamout
                totalamt = amount + shipping_amt
            data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamt':totalamt
            }
            return JsonResponse(data)



@login_required
def Remove_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

        c.delete()
        amount = 0.0
        shipping_amt = 70.0

        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamout = (p.quantity * p.product.discounted_price)
                amount += tempamout

            data={
                'amount':amount,
                'totalamt':amount +shipping_amt
            }
            return JsonResponse(data)
        return HttpResponse('ok')



def search(request):
    query=request.GET['query']
    if len(query)>78:
        allProduct=Product.objects.none()
    else:
        productTitle= Product.objects.filter(title__icontains=query)
        productbrand= Product.objects.filter(brand__icontains=query)
        productcategory =Product.objects.filter(category__icontains=query)
        productdesc=  Product.objects.filter(discription__icontains=query)
        allProduct = productTitle.union(productdesc, productbrand,productcategory)
    if allProduct.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allProduct': allProduct, 'query': query}
    return render(request, 'app/search.html', params)

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        form=CustomerProfileForm()
        return render(request, 'app/profile.html',{'totalitem':totalitem,'form':form,'active':'btn-primary'})

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            #mobile = form.cleaned_data['mobile']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()


            messages.success(request, 'Congratulations !! Profile Add Succesfully')
            return redirect('/address')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


def address_update(request,id):
    p=Customer.objects.get(id=id)
    if request.method=="POST":
        name=request.POST.get('name')
        locality=request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        p.name=name
        p.locality=locality
        p.city=city
        p.state=state
        p.zipcode=zipcode
        p.save()
        messages.success(request, 'Congratulations !! Address update Succesfully')
        return redirect('/address')

    return render(request,'app/profileupdate.html',{'p':p})

@login_required
def address(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'totalitem':totalitem,'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'op':op,'totalitem':totalitem})

@login_required
def change_password(request):


    return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    if data== None:
        mobiles=Product.objects.filter(category='m')
    elif data == 'below':
        mobiles = Product.objects.filter(category='m').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='m').filter(discounted_price__gt=10000)



    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def mobile(request,data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    if data== None:
        mobiles=Product.objects.filter(category='m')
    elif data == 'below':
        mobiles = Product.objects.filter(category='m').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='m').filter(discounted_price__gt=10000)



    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def laptop(request,data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    if data== None:
        laptop=Product.objects.filter(category='L')
    elif data == 'below':
        laptop = Product.objects.filter(category='L').filter(discounted_price__lt=25000)
    elif data == 'above':
        laptop = Product.objects.filter(category='L').filter(discounted_price__gt=23000)



    return render(request, 'app/laptop.html',{'laptop':laptop,'totalitem':totalitem})

def topwear(request,data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    if data== None:
        top=Product.objects.filter(category='TW')
    elif data == 'below':
        top = Product.objects.filter(category='TW').filter(discounted_price__lt=500)
    elif data == 'above':
        top = Product.objects.filter(category='TW').filter(discounted_price__gt=500)



    return render(request, 'app/top.html',{'top':top,'totalitem':totalitem})

def bottomwear(request,data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    if data== None:
        bottom=Product.objects.filter(category='BW')
    elif data == 'below':
        bottom = Product.objects.filter(category='BW').filter(discounted_price__lt=500)
    elif data == 'above':
        bottom = Product.objects.filter(category='BW').filter(discounted_price__gt=500)



    return render(request, 'app/bottom.html',{'bottom':bottom,'totalitem':totalitem})



class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})

    def post(self,request):
        form=CustomRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Ragistered Succesfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amt = 70.0
    totalamt = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamout = (p.quantity * p.product.discounted_price)
            amount += tempamout
            totalamt = amount + shipping_amt


    return render(request, 'app/checkout.html',{'add':add,'totalamt':totalamt,'cart_items':cart_items,'totalitem':totalitem})




@login_required
def paymentdone(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")