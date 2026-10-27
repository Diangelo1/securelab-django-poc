from django.shortcuts import render, redirect
from django.db import connection, DatabaseError
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from .models import UsuarioDemo, PreferenciaDemo

def preparar_dados():
    exemplos = [
        ("Ana Souza", "ana.exemplo@teste.local"),
        ("Bruno Lima", "bruno.exemplo@teste.local"),
        ("Carla Mendes", "carla.exemplo@teste.local"),
    ]
    for nome, email in exemplos:
        UsuarioDemo.objects.get_or_create(nome=nome, defaults={"email": email})
    PreferenciaDemo.objects.get_or_create(nome="tema", defaults={"valor": "azul"})

def inicio(request):
    preparar_dados()
    preferencia = PreferenciaDemo.objects.get(nome="tema")
    return render(request, "laboratorio/inicio.html", {"preferencia": preferencia})

def sql_injection(request):
    preparar_dados()
    termo = request.GET.get("nome", "")
    vulneraveis = []
    protegidos = []
    erro = ""
    consulta = ""
    if termo:
        # VULNERÁVEL DE PROPÓSITO: concatena a entrada dentro do SQL.
        # Este exemplo é somente SELECT e utiliza dados fictícios locais.
        consulta = f"SELECT nome, email FROM laboratorio_usuariodemo WHERE nome = '{termo}'"
        try:
            with connection.cursor() as cursor:
                cursor.execute(consulta)
                vulneraveis = cursor.fetchall()
        except DatabaseError as exc:
            erro = f"Erro SQL na consulta vulnerável: {exc.__class__.__name__}"
        # PROTEGIDO: ORM parametriza os valores em vez de tratá-los como SQL.
        protegidos = list(
            UsuarioDemo.objects.filter(nome=termo).values_list("nome", "email")
        )
    return render(request, "laboratorio/sql_injection.html", {
        "termo": termo,
        "vulneraveis": vulneraveis,
        "protegidos": protegidos,
        "erro": erro,
        "consulta": consulta,
    })

def xss_protegido(request):
    mensagem = request.session.get("mensagem_xss", "")
    if request.method == "POST":
        mensagem = request.POST.get("mensagem", "")[:500]
        request.session["mensagem_xss"] = mensagem
        return redirect("xss_protegido")
    return render(request, "laboratorio/xss.html", {
        "mensagem": mensagem,
        "modo": "protegido",
    })

def xss_vulneravel(request):
    mensagem = request.session.get("mensagem_xss_vulneravel", "")
    if request.method == "POST":
        mensagem = request.POST.get("mensagem", "")[:500]
        request.session["mensagem_xss_vulneravel"] = mensagem
        return redirect("xss_vulneravel")
    # VULNERÁVEL DE PROPÓSITO: mark_safe impede o escape automático do template.
    # Use exclusivamente em localhost com a carga didática indicada no README.
    mensagem_sem_escape = mark_safe(mensagem) if mensagem else ""
    return render(request, "laboratorio/xss_vulneravel.html", {
        "mensagem": mensagem_sem_escape,
    })

def csrf_protegido(request):
    preparar_dados()
    preferencia = PreferenciaDemo.objects.get(nome="tema")
    aviso = ""
    if request.method == "POST":
        valor = request.POST.get("valor", "")
        if valor in ["azul", "verde", "roxo"]:
            preferencia.valor = valor
            preferencia.save()
            return redirect("csrf_protegido")
        aviso = "Selecione uma opção válida."
    return render(request, "laboratorio/csrf.html", {
        "preferencia": preferencia,
        "aviso": aviso,
        "modo": "protegido",
    })

@csrf_exempt
def csrf_vulneravel(request):
    # VULNERÁVEL DE PROPÓSITO: isenta a view da checagem CSRF.
    # Não copie este padrão para sistemas reais. Demonstração somente local.
    preparar_dados()
    preferencia = PreferenciaDemo.objects.get(nome="tema")
    if request.method == "POST":
        valor = request.POST.get("valor", "")
        if valor in ["azul", "verde", "roxo"]:
            preferencia.valor = valor
            preferencia.save()
            return redirect("csrf_vulneravel")
    return render(request, "laboratorio/csrf.html", {
        "preferencia": preferencia,
        "aviso": "",
        "modo": "vulneravel",
    })
