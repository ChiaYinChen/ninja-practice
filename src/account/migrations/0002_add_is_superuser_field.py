# Generated by Django 5.2.3 on 2025-06-26 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(db_default=False, default=False),
        ),
    ]
