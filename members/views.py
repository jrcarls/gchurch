from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .forms import MembroForm
from .models import Membro


@login_required
def index(request):
    paginator = Paginator(Membro.objects.all(), 10)
    page = paginator.get_page(request.GET.get("page"))
    if request.headers.get("HX-Request"):
        return render(request, "members/_table.html", {"membros": page})
    return render(request, "members/index.html", {"membros": page})


@login_required
def criar(request):
    form = MembroForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        response = HttpResponse()
        response["HX-Redirect"] = reverse("members")
        return response
    return render(request, "members/_form.html", {
        "form": form,
        "action_url": reverse("members_criar"),
    })


@login_required
def editar(request, pk):
    membro = Membro.objects.get(pk=pk)
    form = MembroForm(request.POST or None, request.FILES or None, instance=membro)
    if request.method == "POST" and form.is_valid():
        form.save()
        response = HttpResponse()
        response["HX-Redirect"] = reverse("members")
        return response
    return render(request, "members/_form.html", {
        "form": form,
        "membro": membro,
        "action_url": reverse("members_editar", args=[pk]),
    })
