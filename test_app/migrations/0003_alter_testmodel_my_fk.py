# Generated by Django 5.0.4 on 2024-04-21 20:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_alter_testmodel_f1_alter_testmodel_f2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testmodel',
            name='my_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='test_app.testonetomany'),
        ),
    ]