# Generated by Django 2.0 on 2018-11-09 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workerdetails',
            name='skill',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
