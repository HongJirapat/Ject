from django import forms
from .models import Thread
from django.contrib.auth.models import User
from thread.models import Category

class ThreadForm(forms.ModelForm):
    
    class Meta:
        model = Thread
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }
        
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title ต้องมีความยาวอย่างน้อย 5 ตัวอักษร")
        return title
        
class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['name']