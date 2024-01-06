# Generated by Django 4.2.3 on 2024-01-06 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado em')),
                ('active', models.BooleanField(default=True, verbose_name='ativo')),
                ('title', models.CharField(help_text='Digite o título do projeto', max_length=255, unique=True)),
                ('repository_name', models.CharField(blank=True, choices=[
                 ('b', 'Bitbucket'), ('gh', 'Github'), ('gl', 'Gitlab')], max_length=2, null=True)),
                ('repository_url', models.URLField(blank=True, help_text='Digite a url do repositório', null=True)),
                ('gitlab_project_id', models.CharField(blank=True,
                 help_text='Id do repositório no Gitlab', max_length=8, null=True)),
                ('github_token', models.TextField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='projects', to='crm.customer', verbose_name='cliente')),
                ('repository_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.owner')),
            ],
            options={
                'verbose_name': 'Projeto',
                'verbose_name_plural': 'Projetos',
                'ordering': ('title',),
            },
        ),
    ]
