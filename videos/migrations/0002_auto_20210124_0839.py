# Generated by Django 3.1.3 on 2021-01-24 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenes',
            name='background_color',
            field=models.CharField(blank=True, default='#ffffff', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='scenes',
            name='font_color',
            field=models.CharField(blank=True, default='#000000', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='scenes',
            name='keywords',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='scenes',
            name='order',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='scenes',
            name='text',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='scenes',
            name='text_position',
            field=models.CharField(blank=True, default='bottom', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='tags',
            name='tag',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]