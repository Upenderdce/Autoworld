# Generated by Django 5.1.2 on 2024-10-26 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoworld', '0003_dimensions_modelname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dimensions',
            old_name='modelname',
            new_name='Modelname',
        ),
    ]