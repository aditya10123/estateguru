from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import property,property_rent,customer_details,Feedback
from django.core.exceptions import ValidationError

class propertyform(forms.Form):
   name=forms.CharField(max_length=100)
   address=forms.CharField(max_length=100)
   price=forms.FloatField()
   category=forms.CharField(max_length=100)
 
class registrationform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email', 'password1','password2']

        label={
            'username':'Enter Username',
            'first_name':'Enter First Name',
            'last_name':'Enter Last Name',
            'email':'Enter Email',
            'password1':'Enter Password',
            'password2':'Confirm Password'}
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
              'password2':forms.PasswordInput(attrs={'class':'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email


class propertydetailsform(forms.ModelForm):
    class Meta:
        model=property
        fields=['pro_name','pro_address','pro_cat','pro_price','image']
        label={
            'pro_name':'Enter property name',
            'pro_address':'Enter property address',
            'pro_cat':'Enter property category',
            'pro_price':'Enter price',
            'image':'Add image'
    }
        widgets={

             'pro_name':forms.TextInput(attrs={'class':'form-control'}),
             'pro_address':forms.TextInput(attrs={'class':'form-control'}),
             'pro_cat':forms.Select(attrs={'class':'form-control'}),
             'pro_price':forms.NumberInput(attrs={'class':'form-control'}),
             'image':forms.FileInput(attrs={'class':'form-control'}),
        }



class UserauthenticationFormm(forms.Form):
    email = forms.EmailField(label='Enter email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'password']




class property_rent_form(forms.ModelForm):
    class Meta:
        model= property_rent

        fields=['title','description','location','image','image2','image3','image4','bedrooms','bathrooms','carpet_area',
                'price','available']
        
        label={
            'title':'enter property name',
            'description':'enter property information',
            'location':'enter property location',
            'image':  'add photo',
            'image2':'add photo',
            'image3':'add photo',
            'image4':'add photo',
            'bedrooms':'enter numbers of bedroom',
            'bathrooms':'enter numbers of bathroom',
            'carpet_area':'enter carpet area',
            'price':'enter price',
            'available':'enter status'
          }
        





        widgets={
           'title':forms.TextInput(attrs={'class':'form-control'}),
           'description':forms.TextInput(attrs={'class':'form-control'}),
           'location':forms.TextInput(attrs={'class':'form-control'}),
           'image':forms.FileInput(attrs={'class':'form-control'}),
           'image2':forms.FileInput(attrs={'class':'form-control'}),
           'image3':forms.FileInput(attrs={'class':'form-control'}),
           'image4':forms.FileInput(attrs={'class':'form-control'}),
           'bedrooms':forms.NumberInput(attrs={'class':'form-control'}),
           'price':forms.NumberInput(attrs={'class':'form-control'}),
           'bathrooms':forms.NumberInput(attrs={'class':'form-control'}),
           'carpet_area':forms.NumberInput(attrs={'class':'form-control'}),
           
           'available':forms.TextInput(attrs={'class':'form-control'})
                
                
                
                }
   



class Customer_detailsform(forms.ModelForm):
    class Meta:
        model = customer_details
        fields = ["Name","address","city","pincode"]



       


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
