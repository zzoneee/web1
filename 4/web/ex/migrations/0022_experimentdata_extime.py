# Generated by Django 3.1.4 on 2021-04-05 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ex', '0021_auto_20210405_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentdata',
            name='exTime',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
