from django.db import models

from backend.core.models import Active


class Customer(Active):
    name = models.CharField(max_length=255, unique=True, help_text='Digite o nome do cliente')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.name}'

    def get_projects(self):
        return self.projects.all()
