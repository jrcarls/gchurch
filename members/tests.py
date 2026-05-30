from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import MembroForm
from .models import Membro


class MembroModelTest(TestCase):
    def test_criacao_valida(self):
        membro = Membro.objects.create(nome="João Silva")
        self.assertEqual(Membro.objects.count(), 1)
        self.assertEqual(membro.status, Membro.Status.ATIVO)

    def test_str_retorna_nome(self):
        membro = Membro(nome="Maria Souza")
        self.assertEqual(str(membro), "Maria Souza")

    def test_campos_opcionais_nao_quebram(self):
        membro = Membro.objects.create(nome="Pedro")
        self.assertEqual(membro.email, "")
        self.assertEqual(membro.telefone, "")
        self.assertIsNone(membro.celula)


class MembroFormTest(TestCase):
    def test_form_valido_apenas_com_nome(self):
        form = MembroForm(data={"nome": "Ana Paula", "ministerio": "nenhum", "status": "ativo"})
        self.assertTrue(form.is_valid())

    def test_form_invalido_sem_nome(self):
        form = MembroForm(data={"ministerio": "nenhum", "status": "ativo"})
        self.assertFalse(form.is_valid())
        self.assertIn("nome", form.errors)


class MembroViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="teste", password="senha123")

    def test_index_redireciona_sem_login(self):
        response = self.client.get(reverse("members"))
        self.assertRedirects(response, f"/accounts/login/?next={reverse('members')}")

    def test_index_retorna_200_autenticado(self):
        self.client.login(username="teste", password="senha123")
        response = self.client.get(reverse("members"))
        self.assertEqual(response.status_code, 200)

    def test_criar_get_retorna_partial(self):
        self.client.login(username="teste", password="senha123")
        response = self.client.get(reverse("members_criar"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/_form.html")

    def test_criar_post_valido_salva_e_redireciona(self):
        self.client.login(username="teste", password="senha123")
        response = self.client.post(reverse("members_criar"), {
            "nome": "Carlos Lima",
            "ministerio": "nenhum",
            "status": "ativo",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["HX-Redirect"], reverse("members"))
        self.assertEqual(Membro.objects.count(), 1)

    def test_criar_post_invalido_retorna_form_com_erro(self):
        self.client.login(username="teste", password="senha123")
        response = self.client.post(reverse("members_criar"), {
            "ministerio": "nenhum",
            "status": "ativo",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/_form.html")
        self.assertEqual(Membro.objects.count(), 0)

    def test_editar_post_valido_atualiza_membro(self):
        self.client.login(username="teste", password="senha123")
        membro = Membro.objects.create(nome="Nome Antigo")
        response = self.client.post(reverse("members_editar", args=[membro.pk]), {
            "nome": "Nome Novo",
            "ministerio": "nenhum",
            "status": "ativo",
        })
        self.assertEqual(response["HX-Redirect"], reverse("members"))
        membro.refresh_from_db()
        self.assertEqual(membro.nome, "Nome Novo")
