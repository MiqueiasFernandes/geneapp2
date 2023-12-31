# Generated by Django 4.2.7 on 2023-12-19 12:23

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
                ('rmats_readLength', models.FloatField(default=0.1, validators=[django.core.validators.MinValueValidator(20), django.core.validators.MaxValueValidator(500)])),
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
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.CharField(blank=True, max_length=50, null=True)),
                ('ended_at', models.CharField(blank=True, max_length=50, null=True)),
                ('op', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(19)])),
                ('tsp', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(999999)])),
                ('lock', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(999999)])),
                ('arg1', models.CharField(blank=True, max_length=200, null=True)),
                ('arg2', models.CharField(blank=True, max_length=200, null=True)),
                ('arg3', models.CharField(blank=True, max_length=200, null=True)),
                ('arg4', models.CharField(blank=True, max_length=200, null=True)),
                ('arg5', models.CharField(blank=True, max_length=200, null=True)),
                ('arg6', models.CharField(blank=True, max_length=200, null=True)),
                ('arg7', models.CharField(blank=True, max_length=200, null=True)),
                ('arg8', models.CharField(blank=True, max_length=200, null=True)),
                ('arg9', models.CharField(blank=True, max_length=200, null=True)),
                ('payload', models.CharField(blank=True, max_length=9999, null=True)),
                ('end', models.BooleanField(default=False)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('success', models.BooleanField(default=False)),
                ('meta', models.CharField(blank=True, max_length=999, null=True)),
                ('info', models.CharField(blank=True, max_length=999, null=True)),
                ('out', models.CharField(blank=True, max_length=999, null=True)),
                ('log', models.CharField(blank=True, max_length=999, null=True)),
                ('err', models.CharField(blank=True, max_length=999, null=True)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='geneappserver.project')),
            ],
        ),
    ]
