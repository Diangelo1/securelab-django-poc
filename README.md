# SecureLab Django — laboratório acadêmico de segurança web

Projeto didático para demonstrar SQL Injection, XSS e CSRF usando Python + Django.
Use somente localmente, com dados fictícios. As páginas vulneráveis são intencionais e
existem exclusivamente para fins de ensino. Não publique este projeto na internet.

## Requisitos
- Python instalado
- Terminal aberto nesta pasta

## Windows (PowerShell / terminal do VS Code)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Se o PowerShell bloquear a ativação do ambiente, você pode executar sem ativar:
```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abra: http://127.0.0.1:8000/

## Laboratórios
- SQL Injection: `/sql-injection/`
- XSS protegido: `/xss/`
- XSS vulnerável (somente demonstração local): `/xss-vulneravel/`
- CSRF protegido: `/csrf/`
- CSRF vulnerável (somente demonstração local): `/csrf-vulneravel/`

## Como demonstrar
### SQL Injection
Na tela SQL Injection, procure `Ana`. Depois experimente o texto de demonstração:
`' OR '1'='1' -- `
A consulta insegura pode retornar todos os registros fictícios; a consulta protegida procura o texto como um valor literal. O exemplo vulnerável usa apenas SELECT e dados fictícios.

### XSS
Na tela XSS, envie como mensagem:
`<script>alert('XSS de demonstração')</script>`
Na página protegida, o texto aparece como texto e não executa. Na página vulnerável, o navegador interpreta o conteúdo como HTML/JavaScript. Faça isso somente no ambiente local.

### CSRF
Use as páginas de demonstração para alterar uma preferência fictícia. O endpoint protegido exige o token CSRF do Django. O endpoint vulnerável foi intencionalmente isento da validação e serve somente para comparação local.

## Aviso
Nunca use as páginas vulneráveis com dados reais, nunca exponha o servidor na rede e não remova as proteções do projeto real. A configuração de desenvolvimento do Django não é adequada para produção.
