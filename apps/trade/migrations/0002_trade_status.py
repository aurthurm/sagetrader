# Generated by Django 2.2a1 on 2019-01-18 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='status',
            field=models.CharField(choices=[('O', 'Open'), ('C', 'Closed')], default='O', max_length=10, verbose_name='status'),
        ),
    ]