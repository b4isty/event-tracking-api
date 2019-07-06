# Generated by Django 2.2.3 on 2019-07-06 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='type',
        ),
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.ManyToManyField(null=True, related_name='events', to='events.Type'),
        ),
    ]
