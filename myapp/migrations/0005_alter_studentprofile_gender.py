# Generated by Django 4.2.7 on 2023-12-12 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_studentprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], default='Male', max_length=200),
        ),
    ]