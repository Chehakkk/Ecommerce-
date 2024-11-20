from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Cart,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
import random
import razorpay
from django.core.mail import send_mail


# Create your views here.
def home(request):
    context={}
    products = Product.objects.all()   #this will fetch all the records from product table
    context['products'] =  products
    print(context['products'])
    return render(request,"index.html",context)

def viewdetail(request,pid):
    context={}
    product=Product.objects.get(id=pid)
    context['product'] = product
    return render(request,"viewdetail.html",context)

def catfilter(request,cid):
    products=Product.objects.filter(category=cid)
    context={}
    context['products'] = products
    return render(request,"index.html",context)

def sort(request,sid):
    context={}
    if sid=='1':
        products=Product.objects.all().order_by('price')
    elif sid=='0':
        products=Product.objects.all().order_by('-price')
    context['products'] = products    
    return render(request,"index.html",context)
    
def range (request):
    if(request.method=='POST'):
        context={}
        min=request.POST['min']
        max=request.POST['max']
        products=Product.objects.filter(price__gte=min,price__lte=max)
        context['products']=products
        return render (request,'index.html',context)
    else:
        return render(request,'index.html')


def registration (request):
    context={}
    if(request.method=='POST'):
        uname = request.POST['uname']
        upass = request.POST['upass']
        ucpass = request.POST['ucpass']
        if (uname==''or upass==''or ucpass==''):
            context['error']="please fill all the fields"  
            return render(request,"registration.html",context)
        elif (upass!=ucpass):
            context['error']="password should be same "
            return render(request,"registration.html")
        else:
            user_obj=User.objects.create(password=upass,username=uname,email=uname)
            user_obj.set_password(upass)
            user_obj.save()
            context['success']="User registered successfully"
            return render(request,"registration.html",context)
    else:
        return render(request,"registration.html")


def user_login(request):
    context={}
    if(request.method=='POST'):
        uname=request.POST['uname']
        password=request.POST['upass']
        if(uname=='' or password==''):
            context['error']="please fill all the fields"
        u = authenticate(username=uname,password=password)
        if u is not None:
            login(request,u)
            return redirect('/')
        else:
            context['error']= "invalid username or password"
            return render (request,"login.html",context)
    else:
        return render(request,"login.html",context)   
    
def user_logout(request):
    logout(request)
    return redirect("/login")    


def addToCart(request,pid):
    if(request.user.is_authenticated):
        uid=request.user.id
        u=User.objects.get(id=uid)
        p=Product.objects.get(id=pid)
        c=Cart.objects.create(uid=u,pid=p)
        c.save()
        return redirect("/")
    else:
        return redirect("/")
    
def viewcart(request):
    context={}
    user=request.user.id
    c=Cart.objects.filter(uid=user)
    np=len(c)
    sum=0
    for i in c:
        sum=sum+i.pid.price*i.quantity
        print(sum)
        print(np)
        context['np']=np
        context['price']= sum 
        context['products']=c
    return render(request,'cart.html',context)  

def removeFromCart(request,cid):
    Cart.objects.get(id=cid).delete()
    return redirect("/viewcart")

def updateqty(request,qv,cid):
    if request.user.is_authenticated:
        c=Cart.objects.filter(id=cid)
        if qv=='1':
            t=c[0].quantity+1
            c.update(quantity=t)

        elif qv=='0':
            if c[0].quantity>1:
                t=c[0].quantity-1
                c.update(quantity=t)
            elif c[0].quantity == 1:
                c.delete()
        return redirect("/viewcart")   
    else:
        return redirect("/login")
        


    
def placeorder(request):
    if request.user.is_authenticated:
        user = request.user
        c=Cart.objects.filter(uid=user)
        order_id = random.randrange(1000,9999)
        for i in c:
            o=Order.objects.create(order_id=order_id,uid=user,pid=i.pid,quantity=i.quantity)
            o.save()
            i.delete()
        orders = Order.objects.filter(uid=user)
        np=len(orders)
        sum=0
        for i in orders:
            sum=sum+i.pid.price*i.quantity
        context={}
        context['products']=orders 
        context['sum']=sum 
        context['np']=np 
        return render(request,"placeorder.html",context)    
    

def pay(request):
    order=Order.objects.filter(uid=request.user.id)
    sum=0
    for i in order:
        sum=sum+i.pid.price*i.quantity
        oid=i.order_id
    sum=sum*100
    client = razorpay.Client(auth=("rzp_test_zW7NtKv2qBRdJm", "zQsEYklfN5d8PTC72nVC4N7T"))

    data = { "amount": sum, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['payment']=payment
    return render(request,"pay.html",context)    
                                        
def sendusermail(request):
    msg="order placed successfully"
    send_mail(
    "Ekart order",
    msg,
    "dilipkankariya23@gmail.com",
    ["dilipkankariya23@gmail.com"],
    fail_silently=False,
    )       
    return redirect("/")                                  

def dashboard(request):
    context={}   
    m=Product.objects.all()  #fetch all the data from table Msg
    context['data']=m
    print(m)
    return render(request,"table.html",context)


def delete(request,did):
    m=Product.objects.filter(id=did)
    m.delete()
    return redirect("/dashboard")


def edit(request,sid):
    if request.method == "GET":
        m=Product.objects.filter(id=sid)
        context={}
        context['data']=m
        return render(request,"edit.html",context)
    else:
        username = request.POST['uname']
        contact = request.POST['mobile']
        email = request.POST['uemail']
        msg = request.POST['msg']
        m=Product.objects.filter(id=sid).update(name=username,email=email,mobile=contact,msg=msg)
        return redirect("/dashboard")
    

        
