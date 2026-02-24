from django.shortcuts import render
from .models import Task  # Import the Task model we built
from django.shortcuts import render, redirect # Add redirect
from .forms import TaskForm
from django.shortcuts import get_object_or_404 # Add this import at the top
from rest_framework import viewsets
from .serializers import TaskSerializer
from rest_framework import viewsets, permissions # Add permissions import
from .serializers import TaskSerializer


def task_list(request):
    # The Chef grabs all tasks from the Pantry
    tasks = Task.objects.all() 
    
    # The Chef puts the tasks on a "Plate" (Template)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

from django.contrib.auth.decorators import login_required # Add this import

@login_required # This is "The Bouncer" - prevents anonymous users
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False) # 1. Create the task object but don't save to DB yet
            task.author = request.user      # 2. Assign the logged-in user as the author
            task.save()                    # 3. Now save to DB!
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

# UPDATE VIEW
def task_update(request, pk):
    task = get_object_or_404(Task, id=pk) # Find the specific task or show 404 error
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task) # 'instance=task' fills the form with old data
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

# DELETE VIEW
def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == "POST":
        task.delete() # Remove from the Pantry!
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_list(request):
    # Instead of Task.objects.all(), we filter by the current user
    tasks = Task.objects.filter(author=request.user) 
    
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    
    # This ensures ONLY logged-in users can even see the API
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # This ensures you only see YOUR tasks in the JSON response
        return Task.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        # This automatically sets the author when you POST new data to the API
        serializer.save(author=self.request.user)
