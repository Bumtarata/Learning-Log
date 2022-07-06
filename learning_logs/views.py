from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from .functions import check_topic_owner, check_topic_duplicity

def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Show all topics."""
    if request.user.is_authenticated == False:
        topics = Topic.objects.filter(visibility='public')
    else:
        topics = Topic.objects.filter(owner=request.user)|Topic.objects.filter(
            visibility='public')
    topics = topics.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
   
def topic(request, topic_name):
    """Show a single topic and all its entries."""
    if request.user.is_authenticated == False:
        topic = get_object_or_404(Topic, visibility='public', text=topic_name)
    else:
        topic = get_object_or_404(Topic, 
            Q(owner=request.user, text=topic_name)|Q(visibility='public', text=topic_name)
        )
    # Make sure the topic belongs to the current user.
    check_topic_owner(topic, request.user)
        
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required    
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            if check_topic_duplicity(new_topic, request.user):
                new_topic.save()
                return redirect('learning_logs:topics')
            else:
                error_msg = 'Error: Topic of this name already exists.'
                messages.error(request, error_msg)
            
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
 
@login_required 
def new_entry(request, topic_name):
    """Add a new entry for a particular topic."""
    topic = get_object_or_404(Topic, owner=request.user, text=topic_name)
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_name=topic_name)
    
    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)
  
@login_required  
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request.user)
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
        
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_name=topic.text)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)