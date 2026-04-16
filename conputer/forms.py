from django import forms
from .models import PCBuild

class PCBuildForm(forms.ModelForm):
    class Meta:
        model = PCBuild
        # Список полей, которые пользователь будет заполнять
        fields = [
            'title', 'user_name', 'main_photo',
            'cpu', 'gpu', 'motherboard', 'ram', 
            'powerSupply', 'case', 'storage_primary', 
            'cooller', 'coollerCase', 'coollerCase_quantity'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем CSS-классы всем полям для красоты
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'searchField', 'style': 'width: 100%; margin-bottom: 10px;'})