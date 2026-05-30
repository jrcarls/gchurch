from django.db import models


class Membro(models.Model):
    class Ministerio(models.TextChoices):
        LOUVOR = "louvor", "Louvor"
        ENSINO = "ensino", "Ensino"
        INTERCESSAO = "intercessao", "Intercessão"
        DIACONIA = "diaconia", "Diaconia"
        EVANGELISMO = "evangelismo", "Evangelismo"
        INFANTIL = "infantil", "Infantil"
        NENHUM = "nenhum", "Nenhum"

    class Status(models.TextChoices):
        ATIVO = "ativo", "Ativo"
        INATIVO = "inativo", "Inativo"
        VISITANTE = "visitante", "Visitante"

    nome = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    data_batismo = models.DateField(null=True, blank=True)

    logradouro = models.CharField(max_length=200, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)

    celula = models.ForeignKey(
        "groups.Group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="membros",
    )
    ministerio = models.CharField(
        max_length=20,
        choices=Ministerio.choices,
        default=Ministerio.NENHUM,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ATIVO,
    )
    foto = models.ImageField(upload_to="membros/fotos/", null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Membro"
        verbose_name_plural = "Membros"
        ordering = ["nome"]

    def __str__(self):
        return self.nome
