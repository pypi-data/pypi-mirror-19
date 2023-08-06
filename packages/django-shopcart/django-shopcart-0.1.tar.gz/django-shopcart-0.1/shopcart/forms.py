from django import forms

ITEMS = (
    ('mobile', 'Mobile Phone (Rs. 12000)'),
    ('pencil', 'Pencils (Rs. 100)'),
    ('textbooks', 'Text Books (Rs. 2000)'),
    ('shirts', 'Shirts (Rs. 500)'),
)

class ItemsForm(forms.Form):
    store_items = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=ITEMS,
    )
