from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class property_cat(models.Model):
    p_name=models.CharField(max_length=100,unique=True)
    image=models.ImageField(upload_to='static/image', null=True,blank=True)


    def __str__(self):
        return self.p_name
    
class property(models.Model):
    pro_name=models.CharField(max_length=100)
    pro_address=models.CharField(max_length=100)
    pro_cat=models.ForeignKey(property_cat,on_delete=models.PROTECT)

    pro_price=models.DecimalField(max_digits=10,decimal_places=2)
    
    image=models.ImageField(upload_to='images/')

    def __str__(self):
     return self.pro_name


class customer_details(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Name=models.CharField(max_length=100)
    address=models.TextField(blank=True,null=True)
    city=models.CharField(max_length=100)
    pincode=models.IntegerField(default=0,blank=True,null=True)

    def __str__(self):
      return self.user
   
    




class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} ({self.email})"

















class book(models.Model):
   uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
   pid=models.ForeignKey(property,on_delete=models.CASCADE,db_column="pid")
   qty=models.IntegerField(default=1)






class property_rent(models.Model):
   PROPERTY_STATUS = [
      ('available','for available'),
      ('unavailable','for unavailable'),

   ]



   title = models.CharField(max_length=100)
   description =models.TextField()
   image=models.ImageField(upload_to='images/',null=True, blank=True)
   image2=models.ImageField(upload_to='images/',null=True, blank=True)
   image3=models.ImageField(upload_to='images/',null=True, blank=True)
   image4=models.ImageField(upload_to='images/',null=True, blank=True)         
   price = models.DecimalField(max_digits=10, decimal_places=2)
   location = models.CharField(max_length=255)
   bedrooms = models.IntegerField()

   bathrooms = models.IntegerField()

   carpet_area= models.CharField(max_length=100)
   date_listed = models.DateField(auto_now_add=True)

   available= models.CharField(max_length=100,choices=PROPERTY_STATUS)
   deposite_amount=models.DecimalField(max_digits=10, decimal_places=2,null=True,default=True)


   def __str__(self):
      return self.title
   
class rent(models.Model):
   uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
   pid=models.ForeignKey(property_rent,on_delete=models.CASCADE,db_column="pid")
    

class booking(models.Model):
   STATUS_CHOICE = [

      ('PENDING','pending'),
      ('PROCESSING','processing'),
      ('COMPLETE','complete'),
   ]

   customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
   pro_name =models.ForeignKey( property,on_delete=models.CASCADE)
   quantity = models.PositiveIntegerField(default=1)
   price =models.DecimalField(max_digits=10,decimal_places=2, blank=True,null=True)
   booking_date = models.DateTimeField(auto_now_add=True)
   status = models.CharField(max_length=20,choices=STATUS_CHOICE,default='pending')


   def __str__(self):
      return f"payment #{self.id} - {self.status}"

























# class Booking(models.Model):
#      user = models. ForeignKey(User,on_delete=models.CASCADE)
#      flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
#      start_date = models. DateField()
#      end_date = models. DateField()
#      total_price = models.DecimalField(max _digits=10, decimal_places=2)
       
#      def str_(self):
#      return f"Booking by {self.user.username} for {self.flat.title}"

# class Review(models. Model):
#        flat = models.ForeignKey(Flat, on_delete=models. CASCADE, related _name='reviews')
#        user = models.ForeignKey(User, on _delete=models. CASCADE)
#        rating = models IntegerField (choices=[(1, '1'), (2, '2'), (3, '3"), (4, '4*), (5, '5')])
#        comment = models. TextField()
      
#        def_str_(self):
#        return f"Review by {self.user.username} for {self.flat.title}" 