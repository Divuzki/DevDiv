# Generated by Django 4.0.4 on 2022-04-18 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='post',
            name='image_color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
