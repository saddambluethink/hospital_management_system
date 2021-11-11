# Generated by Django 3.2.8 on 2021-10-21 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_auto_20211019_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='prescription',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='dep',
            field=models.CharField(choices=[('Cardiologist', 'Cardiologist'), ('Dermatologists', 'Dermatologists'), ('Allergists', 'Allergists'), ('Anesthesiologists', 'Anesthesiologists')], default='Cardiologist', max_length=50),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='specielist',
            field=models.CharField(choices=[('Cardiologist', 'Cardiologist'), ('Dermatologists', 'Dermatologists'), ('Allergists', 'Allergists'), ('Anesthesiologists', 'Anesthesiologists')], default='Cardiologist', max_length=50),
        ),
    ]
