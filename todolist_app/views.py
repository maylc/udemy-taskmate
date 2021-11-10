from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from todolist_app.forms import TaskForm
from todolist_app.models import TaskList


@login_required
def todolist(request):
    if request.method == 'POST':
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).manager = request.user
            form.save()
        messages.success(request, ("New Task Added!"))
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(manager=request.user)
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)

        context = {'all_tasks': all_tasks}
        return render(request, 'todolist.html', context)


@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)

    if task.manager == request.user:
        task.delete()
    else:
        messages.success(request, "Access Restricted, you are not allowed!")

    return redirect('todolist')


@login_required
def edit_task(request, task_id):
    if request.method == 'POST':
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)

        if form.is_valid():
            form.save()

        messages.success(request, "Task Edited!")
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        context = {'task': task_obj}
        return render(request, 'edit.html', context)


@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.done = True
        task.save()
    else:
        messages.success(request, "Access Restricted, you are not allowed!")

    return redirect('todolist')


@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()

    return redirect('todolist')


def about(request):
    context = {'message': 'Welcome to about page'}
    return render(request, 'about.html', context)


def contact(request):
    context = {'message': 'Welcome to contact page'}
    return render(request, 'contact.html', context)


def index(request):
    context = {'message': 'Welcome to Index page'}
    return render(request, 'index.html', context)
