from django.shortcuts import render
from notes.models import Record
import random


# NOT FINISHED
# Create your views here.
def test(request, pk_topic, pk_note):
    profile = request.user.profile
    topic = profile.topic_set.get(id=pk_topic)
    note = topic.note_set.get(id=pk_note)
    records = note.record_set.all()

    records_ids = Record.objects.filter(note=note).values_list('id', flat=True)\
    #    .values_list('value', flat=True)
    incorrect_answers = dict()
    for record in records:
        choices = []
        while len(choices) < 3:
            choice = random.choice(records_ids)
            choice_record = records.get(id=choice)
            if choice != record.id and choice_record not in choices:
                choices.append(choice_record)
        incorrect_answers[record] = choices
    print(incorrect_answers)

        # print(record_value)
    # print(records_values)

    return render(
        request,
        'tests/test.html',
        context={
            'note': note,
            'records': records,
            'incorrect_answers': incorrect_answers
        }
    )