from django.db import models


class Group(models.Model):
    nome = models.CharField(max_length=100)
    lider = models.CharField(max_length=100)
    dia_reuniao = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=200, blank=True)
    ativa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Célula"
        verbose_name_plural = "Células"
        ordering = ["nome"]

    def __str__(self):
        return self.nome
