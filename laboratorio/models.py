from django.db import models

class UsuarioDemo(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.nome

class PreferenciaDemo(models.Model):
    nome = models.CharField(max_length=50, unique=True, default="tema")
    valor = models.CharField(max_length=50, default="azul")

    def __str__(self):
        return f"{self.nome}: {self.valor}"
