from .models import Account
from django import forms


class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirm Password'
    }))
    class Meta:
        model=Account
        fields=['email','first_name','last_name','password']
    
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'

class AccountForm(forms.ModelForm):
    class Meta:
        model =Account
        fields=['email','first_name','last_name','username','phone']

    def __init__(self,*args,**kwargs):
        super(AccountForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
        
        self.fields['username'].widget.attrs['readonly']=True

        self.fields['email'].widget.attrs['readonly']=True
            