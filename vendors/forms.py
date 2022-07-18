from django import forms
from store.models import Product

class AddProductForm(forms.ModelForm):

    class Meta:
        model=Product
        fields = ['product_name','category','description','price','stock','is_available','author','sub_category','primary_image']
        widgets = {
            "primary_image":forms.ClearableFileInput(attrs={
                "class":"form-control",
                "name":"primary_image",
                "type":"file"
            })
        }

    def __init__(self,*args, **kwargs):
        super(AddProductForm,self).__init__(*args,**kwargs)
        
        self.fields['category'].widget.attrs['class'] = 'form-select'

        self.fields['sub_category'].widget.attrs['class'] = 'form-select'

        self.fields['product_name'].widget.attrs['placeholder'] = 'product name'
        self.fields['product_name'].widget.attrs['class'] = 'form-control'
        self.fields['product_name'].widget.attrs['type'] = 'text'

        self.fields['author'].widget.attrs['placeholder'] = 'author'
        self.fields['author'].widget.attrs['class'] = 'form-control'
        self.fields['author'].widget.attrs['type'] = 'text'

        self.fields['description'].widget.attrs['placeholder'] = 'product description'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['type'] = 'text'
        self.fields['description'].widget.attrs['rows'] = '3'

        self.fields['price'].widget.attrs['placeholder'] = 'price'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['type'] = 'text'
        
        self.fields['stock'].widget.attrs['placeholder'] = 'available stock'
        self.fields['stock'].widget.attrs['class'] = 'form-control'
        self.fields['stock'].widget.attrs['type'] = 'text'

        self.fields['is_available'].widget.attrs['class'] = 'form-check-input'
        self.fields['is_available'].widget.attrs['type'] = 'checkbox ' 
