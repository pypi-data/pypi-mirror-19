from django.forms import ModelForm
from nimble.models.debt import Debt


class DebtForm(ModelForm):

    class Meta:
        model = Debt
        fields = ['title']
