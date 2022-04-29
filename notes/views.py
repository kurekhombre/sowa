from django.shortcuts import render, redirect
from .models import Topic, Note, Record
from .forms import TopicForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='login')
def topic_list(request):
    profile = request.user.profile
    topics = profile.topic_set.all()

    return render(
        request,
        'notes/topic_list.html',
        context={
            'topics': topics
        }
    )


@login_required(login_url='login')
def topic_detail(request, pk):
    profile = request.user.profile
    topic = profile.topic_set.get(id=pk)
    notes = topic.note_set.all()


    return render(
        request,
        'notes/topic_detail.html',
        context={
            'topic': topic,
            'notes': notes
        }
    )


@login_required(login_url='login')
def create_topic(request):
    profile = request.user.profile
    form = TopicForm()

    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.owner = profile
            topic.save()
            messages.success(request, "Topic was added successfully")
            return redirect('topic-list')

    return render(
        request,
        'notes/topic_form.html',
        context={
            'form': form
        }
    )


@login_required(login_url='login')
def update_topic(request, pk):
    page = 'update'
    profile = request.user.profile
    topic = profile.topic_set.get(id=pk)
    form = TopicForm(instance=topic)

    if request.method == "POST":
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, "Topic was edited successfully")

            return redirect('topic-list')

    return render(
        request,
        'notes/topic_form.html',
        context={
            'form': form,
            'page': page,
        }
    )


@login_required(login_url='login')
def delete_topic(request, pk):
    profile = request.user.profile
    topic = profile.topic_set.get(id=pk)

    if request.method == "POST":
        topic.delete()
        messages.success(request, "Topic was deleted successfully")

        return redirect('topic-list')

    return render(
        request,
        'delete_template.html',
        context={
            'object': topic,
        }
    )



@login_required(login_url='login')
def create_note(request, pk):
    profile = request.user.profile
    topic = profile.topic_set.get(id=pk)

    if request.method == "POST":
        data = request.POST
        note = Note.objects.create(
            topic=topic,
            title=data.get('title'),
            summary=data.get('summary')
        )
        keys_list = data.getlist("key")
        values_list = data.getlist("value")
        key_value_dict = dict(zip(keys_list, values_list))
        for key, value in key_value_dict.items():
            Record.objects.create(
                note=note,
                key=key,
                value=value
            )
            messages.success(request, "New note added successfully")
        return redirect('note-update', topic.id, note.id)
    return render(
        request,
        'notes/note_form.html',
        context={
            'topic': topic
        }
    )


@login_required(login_url='login')
def update_note(request, pk_topic, pk_note):
    page = 'update'
    profile = request.user.profile
    topic = profile.topic_set.get(id=pk_topic)
    note = topic.note_set.get(id=pk_note)
    records = note.record_set.all()

    if request.method == "POST":
        data = request.POST
        Note.objects.filter(id=note.id).update(
            topic=topic,
            title=data.get('title'),
            summary=data.get('summary')
        )
        keys_list = data.getlist("key")
        values_list = data.getlist("value")
        key_value_dict = dict(zip(keys_list, values_list))
        Record.objects.filter(note=note.id).delete()
        for key, value in key_value_dict.items():
            Record.objects.update_or_create(
                note=note,
                key=key,
                value=value
            )

        messages.success(request, "New note updated successfully")
        return redirect('note-update', topic.id, note.id)

    return render(
        request,
        'notes/note_form.html',
        context={
            'page': page,
            'topic': topic,
            'note': note,
            'records': records
        }
    )

@login_required(login_url='login')
def delete_note(request, pk_topic, pk_note):
    profile = request.user.profile
    topic = profile.topic_set.get(id=pk_topic)
    note = topic.note_set.get(id=pk_note)

    if request.method == "POST":
        note.delete()
        messages.success(request, "Note was deleted successfully")

        return redirect('topic-list')

    return render(
        request,
        'delete_template.html',
        context={
            'object': note,
        }
    )