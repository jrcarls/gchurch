from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .forms import MembroForm
from .models import Membro


@login_required
def index(request):
    q = request.GET.get("q", "").strip()
    qs = Membro.objects.all()
    if q:
        qs = qs.filter(Q(nome__icontains=q) | Q(email__icontains=q) | Q(telefone__icontains=q))
    paginator = Paginator(qs, 10)
    page = paginator.get_page(request.GET.get("page"))
    context = {"membros": page, "q": q}
    if request.headers.get("HX-Request"):
        return render(request, "members/_table.html", context)
    return render(request, "members/index.html", context)


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
