# Generated by Django 3.1.4 on 2021-04-05 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ex', '0022_experimentdata_extime'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentdata',
            name='report',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ex.report'),
        ),
    ]
