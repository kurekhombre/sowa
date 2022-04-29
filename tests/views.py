from django.shortcuts import render
from notes.models import Record
import random


# Create your views here.
def test(request, pk_topic, pk_note):
    profile = request.user.profile
    topic = profile.topic_set.get(id=pk_topic)
    note = topic.note_set.get(id=pk_note)
    records = note.record_set.all()

    records_values = Record.objects.filter(note=note)
    # print(records_values)
    list = []
    for record in records_values:
        list.append(record.value)
    wrong = random.sample(list, 3)

    for i in range(len(records_values)):
        print(i)
    return render(
        request,
        'tests/test.html',
        context={
            'note': note,
            'records': records,
            'wrong': wrong
        }
    )