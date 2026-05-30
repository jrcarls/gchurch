import random

from django.core.management.base import BaseCommand
from faker import Faker

from groups.models import Group
from members.models import Membro

fake = Faker("pt_BR")


class Command(BaseCommand):
    help = "Popula o banco com dados de membros para desenvolvimento"

    def add_arguments(self, parser):
        parser.add_argument("--total", type=int, default=30)
        parser.add_argument("--clear", action="store_true", help="Remove registros existentes antes de criar")

    def handle(self, *args, **options):
        if options["clear"]:
            Membro.objects.all().delete()
            Group.objects.all().delete()
            self.stdout.write("Registros removidos.")

        celulas = self._criar_celulas()
        self._criar_membros(options["total"], celulas)
        self.stdout.write(self.style.SUCCESS(f"{options['total']} membros criados com sucesso."))

    def _criar_celulas(self):
        nomes = ["Célula Norte", "Célula Sul", "Célula Centro", "Célula Leste", "Célula Oeste"]
        celulas = []
        for nome in nomes:
            celula, _ = Group.objects.get_or_create(
                nome=nome,
                defaults={
                    "lider": fake.name(),
                    "dia_reuniao": random.choice(["Segunda", "Quarta", "Sexta", "Sábado"]),
                    "endereco": fake.address(),
                },
            )
            celulas.append(celula)
        return celulas

    def _criar_membros(self, total, celulas):
        ministerios = [m[0] for m in Membro.Ministerio.choices]
        status_opcoes = [s[0] for s in Membro.Status.choices]
        estados = ["SP", "RJ", "MG", "RS", "BA", "PR", "SC", "GO", "PE", "CE"]

        for _ in range(total):
            Membro.objects.create(
                nome=fake.name(),
                email=fake.email(),
                telefone=fake.phone_number(),
                data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=80),
                data_batismo=fake.date_between(start_date="-20y", end_date="today") if random.random() > 0.3 else None,
                logradouro=fake.street_address(),
                cidade=fake.city(),
                estado=random.choice(estados),
                celula=random.choice(celulas + [None]),
                ministerio=random.choice(ministerios),
                status=random.choices(status_opcoes, weights=[70, 20, 10])[0],
            )
