# Generated by Django 2.0 on 2018-11-10 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_workerdetails_skill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workerdetails',
            name='name',
            field=models.CharField(default='Not saved properly', max_length=100000),
        ),
        migrations.AlterField(
            model_name='workerdetails',
            name='profilelink',
            field=models.CharField(default='Not saved properly', max_length=1000000),
        ),
        migrations.AlterField(
            model_name='workerdetails',
            name='rating',
            field=models.IntegerField(default='Not saved properly', null=True),
        ),
        migrations.AlterField(
            model_name='workerdetails',
            name='skill',
            field=models.CharField(default='Not saved properly', max_length=1000),
        ),
    ]
