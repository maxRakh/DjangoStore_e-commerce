from django import forms
from .models import Order


class AddOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'phohe_number',
            'email',
            'type_of_connection',
            'address',
            'city',
            'country',
            'extra',
        ]
        widgets = {
            'extra': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_of_connection'].empty_label = "Способ связи"