# from myapp.foo.bar import ok_to_post
from django import forms
from category.models import Category,Sub_category
class AddCategoryForm(forms.ModelForm):

    class Meta:
        model=Category
        fields = ['category_name','description','cat_image']
        widgets = {
            "cat_image":forms.ClearableFileInput(attrs={
                "class":"form-control",
                "name":"cat_image",
                "type":"file"
            })
        }

    def __init__(self,*args, **kwargs):
        super(AddCategoryForm,self).__init__(*args,**kwargs)
        
        self.fields['category_name'].widget.attrs['placeholder'] = 'category name'
        self.fields['category_name'].widget.attrs['class'] = 'form-control'
        self.fields['category_name'].widget.attrs['type'] = 'text'

        self.fields['description'].widget.attrs['placeholder'] = 'category description'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['type'] = 'text'
        self.fields['description'].widget.attrs['rows'] = '3'


class AddSubCategoryForm(forms.ModelForm):

    class Meta:
        model=Sub_category
        fields = ['sub_category_name','description','cat_image']
        widgets = {
            "cat_image":forms.ClearableFileInput(attrs={
                "class":"form-control",
                "name":"cat_image",
                "type":"file"
            })
        }

    def __init__(self,*args, **kwargs):
        super(AddSubCategoryForm,self).__init__(*args,**kwargs)
        
        self.fields['sub_category_name'].widget.attrs['placeholder'] = 'category name'
        self.fields['sub_category_name'].widget.attrs['class'] = 'form-control'
        self.fields['sub_category_name'].widget.attrs['type'] = 'text'

        self.fields['description'].widget.attrs['placeholder'] = 'category description'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['type'] = 'text'
        self.fields['description'].widget.attrs['rows'] = '3'