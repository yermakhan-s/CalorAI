# Generated by Django 5.0.8 on 2024-11-18 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_myuser_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='language',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]