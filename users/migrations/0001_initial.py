# Generated by Django 4.0.2 on 2022-02-18 01:39

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(default='/static/default_jpg.png', max_length=3080)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('facebook_link', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter_link', models.CharField(blank=True, max_length=255, null=True)),
                ('instagram_link', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, choices=[('Nigeria', 'Nigeria'), ('USA', 'USA'), ('UK', 'UK'), ('Ghana', 'Ghana'), ('Canada', 'Canada')], max_length=60, null=True)),
                ('about_me', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Text limit is 250', max_length=255, unique=True)),
                ('description', models.CharField(blank=True, help_text='Text limit is 200, and know that this is the post snippet', max_length=200, null=True)),
                ('content', ckeditor.fields.RichTextField()),
                ('image_url', models.CharField(blank=True, max_length=3038, null=True)),
                ('video_url', models.CharField(blank=True, max_length=3000, null=True)),
                ('category', models.CharField(choices=[], default='uncategorized', max_length=50)),
                ('hashtag', models.CharField(blank=True, max_length=150, null=True)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('dislikes', models.ManyToManyField(blank=True, related_name='dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('likes', models.ManyToManyField(blank=True, related_name='comments_likes', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users.post')),
                ('user', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
