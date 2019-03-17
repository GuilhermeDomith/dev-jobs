from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Competencia(models.Model):
    nome = models.CharField(max_length=100)

    def __repr__(self):
        return '<Competencia: %s>'%self.nome


class Profile(User):
    competencias = models.ManyToManyField(Competencia)
    vagas_desejadas = models.CharField(max_length=255)
