from django.forms import ModelForm
from nimble.models.feature import Feature


class FeatureForm(ModelForm):

    class Meta:
        model = Feature
        fields = ['title']
