# Generated by Django 2.2a1 on 2019-01-20 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0006_auto_20190119_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='description',
            field=models.TextField(default='Hey', verbose_name='description'),
            preserve_default=False,
        ),
    ]
