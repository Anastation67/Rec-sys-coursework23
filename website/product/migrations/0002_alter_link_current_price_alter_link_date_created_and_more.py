# Generated by Django 4.0.2 on 2022-04-30 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='current_price',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='date_created',
            field=models.DateField(auto_created=True, blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='link',
            name='old_price',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='price_difference',
            field=models.FloatField(blank=True),
        ),
    ]
