from django.forms import ModelForm

from .models import Topic


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description']
        labels = {
            'title': 'Topic title',
            'description': "Describe your topic"
        }

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
