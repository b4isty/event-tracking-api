# Generated by Django 2.2.3 on 2019-07-06 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20190706_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repo',
            name='url',
            field=models.URLField(null=True, unique=True),
        ),
    ]