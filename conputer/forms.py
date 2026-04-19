from django import forms
from .models import PCBuild

class PCBuildForm(forms.ModelForm):
    class Meta:
        model = PCBuild
        fields = [
            'title', 'main_photo',
            'cpu', 'gpu', 'motherboard', 'ram', 
            'powerSupply', 'case', 
            'storage_primary', 'storage_primary_quantity', # Первый диск
            'storage_second', 'storage_second_quantity',   # ВТОРОЙ ДИСК (проверь это!)
            'cooller', 'coollerCase', 'coollerCase_quantity'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем CSS-классы всем полям для красоты
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'searchField', 'style': 'width: 100%; margin-bottom: 10px;'})