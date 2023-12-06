# Generated by Django 4.2.7 on 2023-12-06 21:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('control', models.CharField(max_length=20)),
                ('treatment', models.CharField(max_length=20)),
                ('path', models.CharField(blank=True, max_length=100, null=True)),
                ('organism', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('online', models.BooleanField(default=False)),
                ('fast', models.BooleanField(default=False)),
                ('status', models.PositiveIntegerField(default=1)),
                ('genome', models.CharField(max_length=200)),
                ('anotattion', models.CharField(max_length=200)),
                ('proteome', models.CharField(max_length=200)),
                ('transcriptome', models.CharField(max_length=200)),
                ('library', models.CharField(max_length=20)),
                ('threads', models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('ram', models.PositiveIntegerField(default=4, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('disk', models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('qvalue', models.FloatField(default=0.05, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('psi', models.FloatField(default=0.1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('acession', models.CharField(max_length=100)),
                ('local_path', models.CharField(blank=True, max_length=100, null=True)),
                ('group', models.CharField(max_length=20)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geneappserver.project')),
            ],
        ),
    ]
