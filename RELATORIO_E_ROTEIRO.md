# Documento-base — Segurança Web com Python e Django

## 1. Objetivo
Este trabalho demonstra três vulnerabilidades comuns em aplicações web — SQL Injection, Cross-Site Scripting (XSS) e Cross-Site Request Forgery (CSRF) — comparando exemplos vulneráveis controlados com proteções oferecidas pelo Django.

## 2. SQL Injection
**Conceito:** ocorre quando dados controlados pelo usuário são incorporados diretamente à estrutura de uma consulta SQL. A entrada pode alterar a lógica da consulta.

**Exemplo vulnerável (somente laboratório):**
```python
consulta = f"SELECT nome, email FROM laboratorio_usuariodemo WHERE nome = '{termo}'"
cursor.execute(consulta)
```
O problema é misturar a entrada com o código SQL.

**Proteção manual:** utilizar consultas parametrizadas, mantendo o SQL separado dos valores. A sintaxe dos parâmetros varia conforme o banco de dados.

**Proteção no Django:** usar o ORM, por exemplo:
```python
UsuarioDemo.objects.filter(nome=termo)
```
O ORM trata o valor como dado, e não como parte da estrutura SQL.

**Princípios relacionados:** confidencialidade e integridade; a disponibilidade também pode ser afetada em alguns cenários.

## 3. Cross-Site Scripting (XSS)
**Conceito:** ocorre quando conteúdo não confiável é inserido numa página e interpretado pelo navegador como HTML ou JavaScript.

**Exemplo vulnerável (somente laboratório):**
```python
from django.utils.safestring import mark_safe
mensagem_sem_escape = mark_safe(mensagem)
```
Marcar conteúdo do usuário como seguro pode desativar o escape automático e permitir que o navegador interprete marcação inserida.

**Proteção manual:** validar o contexto de saída, evitar construir HTML por concatenação e não marcar conteúdo não confiável como seguro.

**Proteção no Django:** os templates escapam automaticamente muitos caracteres especiais quando variáveis são renderizadas normalmente:
```django
{{ mensagem }}
```
Evitar `mark_safe`, `|safe` e HTML construído a partir de conteúdo não confiável. Em casos que exigem HTML fornecido pelo usuário, usar sanitização confiável apropriada ao contexto.

**Princípios relacionados:** confidencialidade e integridade; o impacto depende do que o script consegue acessar ou executar.

## 4. Cross-Site Request Forgery (CSRF)
**Conceito:** um site externo tenta induzir o navegador de uma pessoa a enviar uma requisição indesejada para uma aplicação em que ela está autenticada.

**Exemplo vulnerável (somente laboratório):**
```python
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def alterar_preferencia(request):
    ...
```
A isenção remove a validação CSRF para essa view e não deve ser copiada para operações comuns que alteram estado.

**Proteção manual:** verificar que a requisição de alteração contém um token imprevisível associado à sessão e validar esse token no servidor. Também é importante usar cookies com configurações adequadas; isso não substitui sozinho a validação de token.

**Proteção no Django:** manter `CsrfViewMiddleware` ativo e incluir `{% csrf_token %}` em formulários POST internos:
```django
<form method="post">
    {% csrf_token %}
    ...
</form>
```

**Princípios relacionados:** integridade e autenticidade da ação solicitada.

## 5. Comparação resumida

| Vulnerabilidade | Falha típica | Proteção manual | Recurso Django | Princípios relacionados |
|---|---|---|---|---|
| SQL Injection | Entrada altera a consulta SQL | Consultas parametrizadas | ORM / parâmetros | Confidencialidade, integridade |
| XSS | Conteúdo vira código no navegador | Escape contextual e sanitização quando necessária | Escape automático de templates | Confidencialidade, integridade |
| CSRF | Requisição externa tenta provocar ação usando sessão da vítima | Token validado no servidor | Middleware e `{% csrf_token %}` | Integridade, autenticidade |

## 6. Conclusão
Usar um framework não elimina automaticamente vulnerabilidades. O desenvolvedor precisa compreender os recursos de segurança, manter as proteções ativas e evitar desativá-las sem justificativa. O Django oferece ferramentas que ajudam a reduzir esses riscos quando usadas corretamente.

## 7. Roteiro para apresentação de até 10 minutos
- **0:00–1:00 — Introdução:** explicar objetivo, linguagem Python e framework Django.
- **1:00–3:00 — SQL Injection:** explicar entrada misturada com SQL; demonstrar a busca vulnerável e a busca protegida.
- **3:00–5:00 — XSS:** publicar o exemplo de texto no modo protegido e comparar com a rota vulnerável, apenas em localhost.
- **5:00–7:00 — CSRF:** alterar a preferência fictícia nas rotas protegida e vulnerável; explicar token e middleware.
- **7:00–8:30 — Princípios:** resumir confidencialidade, integridade e autenticidade.
- **8:30–10:00 — Conclusão:** reforçar que as rotas vulneráveis são demonstrações, e não padrões aceitáveis para produção.

## 8. Referências para completar conforme o padrão exigido pela instituição
- Django Software Foundation. *Django documentation: Security*. https://docs.djangoproject.com/en/stable/topics/security/
- Django Software Foundation. *Django documentation: Cross site request forgery protection*. https://docs.djangoproject.com/en/stable/ref/csrf/
- OWASP Foundation. *SQL Injection Prevention Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- OWASP Foundation. *Cross Site Scripting Prevention Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- OWASP Foundation. *Cross-Site Request Forgery Prevention Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
