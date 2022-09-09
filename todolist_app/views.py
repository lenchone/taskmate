from multiprocessing import context, managers
from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from django.contrib import messages
from django.core.paginator import Paginator
from todolist_app.forms import TaskForm
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def todolist(request):
    if request.method=="POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request,("New Task added succesfully"))
        return redirect('todolist')
    else:
        # all_tasks=TaskList.objects.all() //fetch all
        
        all_tasks=TaskList.objects.filter(manage=request.user)
        paginator=Paginator(all_tasks,5)
        page=request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        
        return render(request,'todolist.html',{'all_tasks':all_tasks})
    
@login_required
def delete_task(request,task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request,("Access Restricted, You are not allowed"))
    return redirect('todolist')

@login_required
def edit_task(request,task_id):
    if request.method=="POST":
        task = TaskList.objects.get(pk=task_id)
        form= TaskForm(request.POST or None,instance=task)
        if form.is_valid():
            form.save()
        messages.success(request,("Task edited succesfully"))
        return redirect('todolist')
    else:
        task_obj=TaskList.objects.get(pk=task_id)

        return render(request,'edit.html',{'task_obj':task_obj})

@login_required
def complete_task(request,task_id):
    task = TaskList.objects.get(pk=task_id)
    
    if task.manage == request.user:
        task.done=True
        task.save()
    else:
        messages.error(request,("Access Restricted, You are not allowed"))
    return redirect('todolist')

@login_required
def pending_task(request,task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done=False
    
    task.save()
    return redirect('todolist')


# index
def index(request):
    # return HttpResponse("Hello Rochak!")
    context={
             'index_text':"Well Come Index",
             
            } 
    return render(request,'index.html',context)
# index ends here

def contact(request):
    # return HttpResponse("Hello Rochak!")
    context={
             'contact_text':"Well Come to Todo App Jina2 Contact",
             
            }
    return render(request,'contact.html',context)

def about(request):
    # return HttpResponse("Hello Rochak!")
    context={
             'about_text':"Well Come to Todo App Jina2 About",
             
            } 
    return render(request,'about.html',context)