from django.shortcuts import render,HttpResponse,redirect
from .models import property_cat,property,book,property_rent,booking,customer_details,rent
from .forms import propertyform,registrationform,propertydetailsform,UserauthenticationFormm,property_rent_form,Customer_detailsform,FeedbackForm
import datetime
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views import View
from django.conf import settings
import uuid
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView  
from django.views.generic.edit import UpdateView 

from django.urls import reverse_lazy
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import properserializer

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.contrib import messages


import datetime
def logindetails(request):
     if request.method=="POST":
        uemail=request.POST["email"]
        upass=request.POST["password"]
        # user=authenticate(request,email=uemail,password=upass)
        users = get_user_model().objects.filter(email=uemail)
        for user in users:
            if user.check_password(upass):
                user=user
        if user is not None:
            login(request,user)
            
            response=redirect('home')
            request.session['email']=uemail
            response.set_cookie('email',uemail)

            response.set_cookie('time',datetime.datetime.now())
            return response            
        else:
             fm=UserauthenticationFormm()

             return render(request,'login.html',{'forms':fm,'msg':'wrong Credentials!!'})

     else:
         fm=UserauthenticationFormm()
         print(fm)
         return render(request,'login.html',{'forms':fm})  


def logoutdetails(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == "POST":
        u = registrationform(request.POST)
        if u.is_valid():
            u.save()
            return redirect('login')
    else:
        u = registrationform()
    return render(request, 'register.html', {"forms": u})



def show(request):
    proper=property_cat.objects.all()
    pro=property.objects.all()
    rent=property_rent.objects.all()
    context={}
    context['pro']=pro
    context['proper']=proper
    context['rent']=rent

    return render(request,'index.html',context)


def searchproperty(request):
    if request.method=="POST":
        data=request.POST['search']
        print(data)

        searchdata=property.objects.filter(pro_name__icontains=data)
        return render(request,'search.html',{'searchdata':searchdata})
    

    else:
        return redirect('home')
    





def properties_view(request,id):
    proper=property_cat.objects.all()
    pro=property.objects.filter(pro_cat=id)
    context={}
    context['proper']=proper
    context['pro']=pro

    return render(request,'buy.html',context)






def visitpro(request,id):
    pro=property.objects.filter(id=id)
    context={}
    context['pro']=pro
    return render(request,'product.html',context)








def propertyview(request):
    if request.method=="POST":
    
       fm=propertyform(request.POST)
       if fm.is_valid():
           return HttpResponse("DATA IS SAVED")
       
    else:

        fm=propertyform()
        return render (request,"propertyform.html",{'forms':fm})



# class user_login(View):
#     def get(request):
#          fm=UserauthenticationForm()
#          return render(request,'login.html',{'forms':fm})


#     def post(request):
#       if request.method=="POST":
#          uname=request.POST["username"]
#          upass=request.POST["password"]
#          user=authenticate(request,username=uname,password=upass)
#          if user is not None:
#             login(request,user)
            
#             response=render(request,'index.html',{'username':uname})
#             request.session['username']=uname
#             response.set_cookie('username',uname)

#             response.set_cookie('time',datetime.datetime.now())
#             return response            
#          else:
#              fm=UserauthenticationForm()

#              return render(request,'login.html',{'forms':fm,'msg':'wrong Credentials!!'})

def propertydetails(request):
    if request.method=="POST":
        ap=propertydetailsform(request.POST,request.FILES)
        if ap.is_valid():
            ap.save()
            return HttpResponse("Successfully saved")
    else:
        ap=propertydetailsform()
        return render(request,'propertyform.html',{'ap':ap})



@login_required(login_url='login')
def bookproperty(request,pid):
    if request.user.is_authenticated:
     
       userid=request.user.id
    #    print(userid)
    #    print(pid)
       u=User.objects.filter(id=userid)
    #    print(u[0])
       p=property.objects.filter(id=pid)
    #    print(p[0])
       q1=Q(uid=u[0])
       
       b=book.objects.filter(Q(uid=u[0]) & Q(pid=p[0]))
       print(b)
       n=len(b)
       context={}
       context={'pro':p}
       if n==1:
           context['msg']='property is already in  booking list'
           return render(request,'product.html',context)
       
       else:
           b=book.objects.create(uid=u[0],pid=p[0])
           b.save()
           context['success']='property added successfully to book'
           return render(request,"product.html",context)


    #    b=book.objects.create(uid=u[0],pid=p[0])
    #    b.save()

    #    return HttpResponse("bookproperty.html")

   
    






@login_required(login_url='login')
def bookrentproperty(request,pid):
    if request.user.is_authenticated:
     
       userid=request.user.id
    #    print(userid)
    #    print(pid)
       u=User.objects.filter(id=userid)
    #    print(u[0])
       p=property_rent.objects.filter(id=pid)
    #    print(p[0])
       q1=Q(uid=u[0])
       
       b=rent.objects.filter(Q(uid=u[0]) & Q(pid=p[0]))
       print(b)
       n=len(b)
       context={}
       context={'data':p}
       if n==1:
           context['msg']='property is already in  booking list'
           return render(request,'rentpropertyview.html',context)
       
       else:
           b=rent.objects.create(uid=u[0],pid=p[0])
           b.save()
           context['success']='property added successfully to book'
           return render(request,"rentpropertyview.html",context)

def viewproperty(request): 
       userid=request.user.id
       print(userid)
       data=book.objects.filter(uid=userid)
       total=0
       for x in data:
           total=total+x.pid.pro_price*x.qty #price is calculated by pid which ic cart model pid related to price
       context={}
       context['data']=data
       context['total']=total
       return render(request,"book.html",context)

def viewrentproperty(request): 
       userid=request.user.id
       print(userid)
       data=rent.objects.filter(uid=userid)
       total=0
       for x in data:
           total=total+x.pid.price #price is calculated by pid which ic cart model pid related to price
       context={}
       context['data']=data
       context['total']=total
       return render(request,"rentpropertycart.html",context)
    








def remove_property(request,id): 
    c= book.objects.filter(id=id)
    c.delete()
    return redirect('viewproperty')

def remove_rentproperty(request,id): 
    c= rent.objects.filter(id=id)
    c.delete()
    return redirect('viewrentproperty')

def updateproperty(request,qv,cid):
    print(cid)
    print(qv)
    data=book.objects.filter(id=cid)
    if qv==1:
        total_quantity=data[0].qty+1
        data.update(qty=total_quantity)
    else:

         if data[0].qty>1:
    
           total_quantity=data[0].qty-1
           data.update(qty=total_quantity)
 
    return redirect('/viewproperty')






def rent_property(request):
     rent=property_rent.objects.all()
     context={}
     context['rent']=rent

     return render(request,"rent_property.html",context)








def buy_property(request):
    pro=property.objects.all()
    context={}
    context['pro']=pro
    return render(request,"buy.html",context)









def set_cookie(request):
    response=HttpResponse("cookie set")
    response.set_cookie('username','Priya')
    return response

def get_cookie(request):
    username=request.COOKIES.get('username')
    
    print(username)
    return render(request,'getcookie.html',{'username':username})






def feedback_form(request):
    return render(request,'feedback.html')


def contactus_form(request):
    return render(request,'contactus.html')




def rentpropertydetails(request):
    if request.method=="POST":
        ap=property_rent_form(request.POST,request.FILES)
        if ap.is_valid():
            ap.save()
            return HttpResponse("Successfully saved")


    else:
        ap=property_rent_form()
        return render(request,'propertyrentform.html',{'ap':ap})
    






def rent_propertydetails(request,id): 

       data=property_rent.objects.filter(id=id)
       total=0
       for x in data:
           total=total+x.price #price is calculated by pid which ic cart model pid related to price


       context={}
       context['data']=data
       context['total']=total
       
       return render(request,"rentpropertyview.html",context)









def checkoutview(request):
       userid=request.user.id
       c=book.objects.filter(uid=userid)
       total=0
       
       for x in c:
         print (x.pid)
         print (x.uid)
         print (x.qty)
         total_price=total+x.pid.pro_price*x.qty
       print(total_price)
       
      
       host = request.get_host()

       paypal_checkout = {
            'business' : settings.PAYPAL_RECEIVER_EMAIL,
            'amount' :total_price,
            'property_name':'property',
            'invoice':uuid.uuid4(),
            'current_code':'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url' : f"http://{host}{reverse('paymentsuccess')}",
            'cancel_url': f"http://{host}{reverse('paymentfailed')}",
           }
       paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
        
       return render(request,'checkout.html',{'total_price':total_price,'cart_data':c,'paypal':paypal_payment})


def checkoutview1(request):
       userid=request.user.id
       c=rent.objects.filter(uid=userid)
       total=0
       
       for x in c:
         print (x.pid)
         print (x.uid)
     
         total_price=total+x.pid.price
       print(total_price)
       
      
       host = request.get_host()

       paypal_checkout = {
            'business' : settings.PAYPAL_RECEIVER_EMAIL,
            'amount' :total_price,
            'property_name':'property',
            'invoice':uuid.uuid4(),
            'current_code':'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url' : f"http://{host}{reverse('paymentsuccess')}",
            'cancel_url': f"http://{host}{reverse('paymentfailed')}",
           }
       paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
        
       return render(request,'checkout1.html',{'total_price':total_price,'cart_data':c,'paypal':paypal_payment})




def forget_password(request):
    if request.method =='POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user: 
            
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')
                                                   
            send_mail(
            'Password Reset',
            f'Click the given link to reset your password: {reset_url}',
            'adityapawar4844@gmail.com', # Use a verified email address
            [email],
            fail_silently=False,
             )
            return redirect('passwordresetdone')
        else:
           
           
           messages.success(request,'please enter valid email address')

    return render(request,'forgetpass.html')

def reset_password(request, uidb64, token):

    if request.method == 'POST':
       
       password = request.POST['password']
       print(password)
       password2 = request.POST['password2']
       print(password2)
       if password == password2:  
        try:
      
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
             
             user.set_password(password)
             user.save()
             return redirect('passwordresetdone')
            else: 
             return HttpResponse('Token is invalid',status=400)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
           return HttpResponse('Invalid link', status=400)
       else:
          
          return HttpResponse('Passwords do not match', status=400)
    return render(request,'password_rest.html')


def password_reset_done(request):
    return render (request,'password_reset_done.html')














#----------payal code --------------------
      
        
        
   
def paymentsuccess(request):
    pass

def paymentfailed(request):
    pass






def customer_address(request):

     if request.method=="POST":
       
       fm=Customer_detailsform(request.POST)
       name=request.POST['name']
       city =request.POST['city']
       state = request.POST['state']
       pincode=request.POST['pincode']
       context={}
       if name=="" or city=="" or state=="":

          context['errmsg']="Field cannot be empty"
          return render(request,'address.html',context)
       if fm.is_valid():
          data=fm.save(commit=False)
          data.user=request.user
          data.save()
          return redirect('home')
     else:
       mf =Customer_detailsform()
       return render(request,'address.html',{'form':mf})

def checkout(request):
    cust_deatils=customer_details.objects.filter(user=request.user)
    return render(request,'checkout.html',{'cust_details':cust_deatils})
   



# def payment(request):
#        userid=request.user.id
#        print(userid)
#        data=book.objects.filter(uid=userid)
#        total=0
#        for x in data:
         
#          total=total+x.pid.pro_price*x.qty #price is calculated by pid which ic cart model pid related to price


#        context={}
#        context['data']=data
#        context['total']=total
#        return render(request,"payment.html",context)


class PostListView(ListView):
    model= property
    template_name = 'show_property.html'
    context_object_name ='posts'
    paginate_by = 10




class PostCreateView(CreateView):
    model = customer_details
    fields = ['user','Name','address','city','pincode']
    template_name= 'show_property.html'
    success_url= reverse_lazy('showlist')


class PostUpdateView(UpdateView):
    model = customer_details
    fields = ['user','Name','address','city','pincode']
    template_name= 'show_property.html'
    success_url= reverse_lazy('showlist')

#  # retal properties in indexpage

 
class crud_api(APIView):
 
 def post(self,request):
        data=request.data
        print(data)
        serializer=properserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success":"data is successfully saved"},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

 def get(self,request):
        id=request.data.get('id',None)
        print(id)
        if id:
            try:
                properties_data=property.objects.get(id=id)
                serializer=properserializer(properties_data)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except:
                return ResourceWarning({"ERROR":"id is not found"},status=status.HTTP_404_NOT_FOUND)
        
        else:
            properties_data=property.objects.all()
            print(properties_data)
            serializer=properserializer(properties_data,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
            
def patch(self,request):
        update_data=request.data
        print(update_data)
        id=request.data.get("id")
        if id:
             
             properties_data=rentpropertydetails.get(id=id)
             print( properties_data)
             serializer=properserializer(properties_data,update_data,partial=True)
             if serializer.is_valid():
                 serializer.save()
                 return Response({"Successs":"data update successfully"},status=status.HTTP_200_OK)
        

      
def delete(self,request):
        id=request.data.get("id")
        print(id)
        properties_data=property.get(id=id)
        if id:
            properties_data.delete()
            return Response({"success":"successfully deleted"},status=status.HTTP_200_OK)
 



from .forms import FeedbackForm

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')  # Redirect to a 'Thank You' page
    else:
        form = FeedbackForm()

    return render(request, 'feedback_form.html', {'form': form})


def thank_you(request):
    return render(request, 'feedback/thank_you.html')
