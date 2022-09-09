from django.shortcuts import render
from notes.models import Record
import random


def test(request, pk_topic, pk_note):
    profile = request.user.profile
    topic = profile.topic_set.get(id=pk_topic)
    note = topic.note_set.get(id=pk_note)
    records = note.record_set.all()
    records_ids = Record.objects.filter(note=note).values_list('id', flat=True)

    exercise = dict()

    for record in records:
        choices = []
        while len(choices) < 3:
            choice = random.choice(records_ids)
            choice_record = records.get(id=choice)
            if choice != record.id and choice_record not in choices:
                choices.append(choice_record)
        choices.append(record)
        random.shuffle(choices)
        exercise[record] = choices

    if request.method == 'POST':
        data = request.POST

        # MUST CORRECT THIS CODE

        questions = data.getlist('question')
        answers = data.getlist('answer')
        dictionary_of_qa = dict(zip(questions, answers))

        records_queryset = Record.objects.filter(note=note).values_list('key', 'value')
        records_dict = {}
        for record_id in records_queryset:
            records_dict[record_id[0]] = record_id[1]

        qa_keys = set(dictionary_of_qa.keys())
        record_keys = set(records_dict.keys())

        shared_keys = qa_keys.intersection(record_keys)
        same = set(o for o in shared_keys if dictionary_of_qa[o] == records_dict[o])
        different = set(x for x in shared_keys if dictionary_of_qa[x] != records_dict[x])


        score = len(same)
        total = len(records_queryset)
        correct_answers_percent = score / total * 100
        return render(request, 'tests/score.html', {'score': score, 'total': total, 'percent': correct_answers_percent,
                                                    'wrong': different})

    return render(
        request,
        'tests/test2.html',
        context={
            'note': note,
            'records': records,
            'exercise': exercise
        }
    )
