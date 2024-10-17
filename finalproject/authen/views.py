from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView


class LoginView(View):
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('thread-list')
        
        messages.error(request, "ชื่อหรือรหัสผ่านไม่ถูกต้อง")
        return render(request,'login.html', {"form":form})


class LogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('login')
    

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html' # แสดง Template สำหรับลงทะเบียน
    success_url = reverse_lazy('login') # URL ที่จะเปลี่ยนไปหลังจากลงทะเบียนสำเร็จ

    def form_valid(self, form):
        # บันทึกข้อมูล user ใหม่
        response = super().form_valid(form)

        # ดึงกลุ่มที่ต้องการ
        group = Group.objects.get(name='Usergroup')
        self.object.groups.add(group)

        return response

