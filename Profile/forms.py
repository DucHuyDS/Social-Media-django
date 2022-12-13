from .models import Profile
from django import forms

class ProfileForm(forms.ModelForm):
    born=forms.DateField(required=False,widget=forms.DateInput(attrs={
        'type':'date'
    }))
    img=forms.ImageField(widget=forms.FileInput())
    cover_img=forms.ImageField(widget=forms.FileInput())
    class Meta:
        model=Profile
        exclude=('user','friends')
        

    def __init__(self, *args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

