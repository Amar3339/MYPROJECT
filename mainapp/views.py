from django.shortcuts import render ,redirect
from .models import Enquiry, LoginInfo,UserInfo
from django.contrib import messages
from adminapp.models import *
from userapp.models import UserInfo
# Create your views here.
def index(request):
    books=Book.objects.all()
    return render(request,'index.html',{'books':books})

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        enq=Enquiry(name=name,email=email,contact=contact,subject=subject,message=message)
        enq.save()
        messages.success(request,'your enquiry is submitted ')
        return redirect('contact')
    return render(request, 'contact.html')





def adminlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            ad=LoginInfo.objects.get(usertype='user', username=username, password=password)
            if ad is not None:
                request.session['adminid']=username 
                
                messages.success(request,'admin Login Successfully!')
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request,'invalid username or password')
            return redirect('adminlogin')
    return render(request,'userdash.html')



def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if password!=cpassword:
            message.error(request,'password and confirm password ae not matchhing')
            return redirect('register')
        ch=LoginInfo.objects.filter(username=email)
        if ch:
            messages.error(request,'email is alreday registered')
            return redirect('register')
        log=LoginInfo(usertype='user',username=email,password=password)
        user=UserInfo(name=name,email=email,contact=contact,login=  log)
        log.save()
        user.save()
        messages.success(request,'user registered succcessfully')
        return redirect('register')
    
    
        
        
    return render(request,'register.html')

# def login(request):

#     if request.method == "POST":

#         email = request.POST['email']

#         password = request.POST['password']

#         try:

#             user = LoginInfo.objects.get(username=email, password=password)

#             request.session['user_email'] = user.username

#             return redirect('/')
#         except LoginInfo.DoesNotExist:

#             return render(request, 'login.html', {'msg':'Invalid Email or Password'})

#     return render(request, 'login.html')
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = UserInfo.objects.get(email=email, password=password)

            # session create
            request.session["userid"] = user.id
            request.session["username"] = user.name

            messages.success(request, "Login Successful")
            return redirect("/")

        except UserInfo.DoesNotExist:
            messages.error(request, "Invalid Email or Password")

    return render(request, "login.html")

def book_details(request,id):
    book=Book.objects.get(id=id)
    return render(request,'book_details.html',{'book':book})


# Create your views here.
