# Generated by Django 4.0.2 on 2022-05-31 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_link_monitored'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='link',
            options={'ordering': ['date_created']},
        ),
        migrations.AddField(
            model_name='link',
            name='image',
            field=models.FileField(null=True, upload_to='product-thumbnails', verbose_name='photo'),
        ),
    ]
