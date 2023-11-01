# Generated by Django 4.2.5 on 2023-11-01 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets_app', '0003_alter_tickets_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='finish_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='last_used',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='ticket_date',
            field=models.DateTimeField(),
        ),
    ]
