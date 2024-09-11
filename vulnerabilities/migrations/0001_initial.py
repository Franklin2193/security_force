# Generated by Django 5.1.1 on 2024-09-09 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cve_id', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('severity', models.CharField(max_length=50)),
                ('fixed', models.BooleanField(default=False)),
            ],
        ),
    ]
