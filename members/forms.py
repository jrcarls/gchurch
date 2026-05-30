from django import forms

from .models import Membro


class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = [
            "nome",
            "email",
            "telefone",
            "data_nascimento",
            "data_batismo",
            "logradouro",
            "cidade",
            "estado",
            "celula",
            "ministerio",
            "status",
            "foto",
        ]
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date"}),
            "data_batismo": forms.DateInput(attrs={"type": "date"}),
        }
