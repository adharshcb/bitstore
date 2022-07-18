from django import forms
from .models import Account, UserProfile

class UserRegistration (forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number','password']

    def clean(self):
        cleaned_data = super(UserRegistration,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")
        return cleaned_data
    

    def __init__(self,*args, **kwargs):
        super(UserRegistration,self).__init__(*args,**kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control p-3'

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number']
    
    def __init__(self,*args, **kwargs):
        super(UserForm,self).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'




class UserProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False,error_messages={'invalid':("Image files only")},widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['address_line_1','address_line_2','profile_image','city','state','country']

    def __init__(self,*args, **kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Address line 1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Address line 2'
        self.fields['profile_image'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['country'].widget.attrs['placeholder'] = 'country'
        self.fields['state'].widget.attrs['placeholder'] = 'state'
        self.fields['city'].widget.attrs['placeholder'] = 'city'
        self.fields['profile_image'].widget.attrs['class'] = ''
