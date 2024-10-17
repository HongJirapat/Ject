from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views import View
from thread.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from thread.forms import *


def is_my_thread(user, author):
    if user == author:
        return True
    return False


class ThreadListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ["thread.view_thread"]
    
    def get(self, request: HttpRequest):
        thread = Thread.objects.all()
        categories = Category.objects.all()
        
        selected_category = request.GET.get('category')  # เอาค่าจาก query string
        if selected_category:
            thread = thread.filter(category__id=selected_category)
            
        context = {
            "threads": thread,
            "categories": categories,
            "selected_category": selected_category,
        }
        return render(request, 'thread_list.html', context)


class ThreadDetailView(LoginRequiredMixin, View):
    login_url = '/authen/'

    def get(self, request: HttpRequest, pk):
        thread = get_object_or_404(Thread, pk=pk)
        comments = Comment.objects.filter(thread=thread).order_by('created_at')
        return render(request, 'thread_detail.html', {
            'thread': thread,
            'comments': comments,
        })

    def post(self, request: HttpRequest, pk):
        thread = get_object_or_404(Thread, pk=pk)
        content = request.POST.get('content')
        
        if content:
            comment = Comment.objects.create(
                content=content,
                author=request.user,
                thread=thread
            )
            comment.save()

        return redirect('thread-detail', pk=pk)
    

class ThreadCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ["thread.add_thread"]

    def get(self, request: HttpRequest):
        form = ThreadForm()
        categories = Category.objects.all()
        context = {
            "form": form,
            "categories": categories,
        }
        return render(request, 'thread_create.html', context)

    def post(self, request: HttpRequest):
        form = ThreadForm(request.POST)

        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()

            # ดึง category ที่ถูกเลือกมาจาก checkbox
            selected_categories = request.POST.getlist('category')
            if selected_categories:
                for category_id in selected_categories:
                    category = Category.objects.get(id=category_id)
                    thread.category.add(category)  # เพิ่ม category ให้ thread

            form.save_m2m()
            return redirect('thread-list')
        else:
            return render(request, "thread_create.html", {"form": form})

        
class CreateCategoryView(LoginRequiredMixin, View):
    login_url = '/authen/'
    
    def post(self, request):
        category_name = request.POST.get('name', None)
        
        if category_name:
            if not Category.objects.filter(name=category_name).exists():
                # สร้าง category ถ้ายังไม่มีในระบบ
                Category.objects.create(name=category_name)
                return JsonResponse({'success': True})
            else:
                # ถ้ามี category ชื่อซ้ำกัน
                return JsonResponse({'error': 'Category name already exists.'}, status=400)
        else:
            # ถ้าชื่อ category ไม่ถูกต้องหรือไม่มีการส่งมา
            return JsonResponse({'error': 'Invalid category name'}, status=400)
        
        
class ThreadHistoryView(LoginRequiredMixin, View):
    login_url = '/authen/'

    def get(self, request):
        if request.user.is_staff:
            threads = Thread.objects.all()
        else:
            my_threads = Thread.objects.filter(author=request.user) 

        context = {
            'my_threads': my_threads if not request.user.is_staff else None,
            'threads': threads if request.user.is_staff else None,
        }
        return render(request, 'thread_history.html', context)

        

class ThreadEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ["thread.change_thread"]
    
    def get(self, request: HttpRequest, pk):
        thread = get_object_or_404(Thread, pk=pk)
        form = ThreadForm(instance=thread)  # สร้างฟอร์มจาก instance ของกระทู้
        return render(request, "thread_edit.html", {"form": form, "thread": thread})

    def post(self, request: HttpRequest, pk):
        thread = get_object_or_404(Thread, pk=pk)
        
        if not is_my_thread(request.user, thread.author):
            raise PermissionDenied("Only for the blog owner.")
        
        form = ThreadForm(request.POST, instance=thread)
        
        if form.is_valid():
            form.save()
            return redirect('thread-list')
        else:
            context = {
                "thread": thread,
                "form": form  
            }
            return render(request, "thread_edit.html", context)


class ThreadDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/authen/'
    permission_required = ["thread.delete_thread"]

    def post(self, request: HttpRequest, pk):
        thread = get_object_or_404(Thread, pk=pk)
        thread.delete()
        return redirect('thread-list')


        
