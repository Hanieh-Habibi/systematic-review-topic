# Generated by Django 4.0.4 on 2022-04-18 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=256)),
                ('doi', models.CharField(default='', max_length=256)),
                ('abstract', models.CharField(max_length=4096)),
                ('full_text', models.TextField()),
                ('publication', models.DateField()),
                ('url_file', models.URLField(null=True)),
                ('is_file_get', models.BooleanField(default=False)),
                ('pmcid', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=128)),
                ('first_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(max_length=256)),
                ('year_begin', models.DateField()),
                ('year_end', models.DateField()),
                ('step', models.CharField(choices=[('article', 'Article'), ('processing', 'Processing'), ('clustering', 'Clustering')], default='article', max_length=64)),
                ('is_finish', models.BooleanField(default=False)),
                ('is_error', models.BooleanField(default=False)),
                ('error', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='TableChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_display', models.BooleanField(default=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.article')),
                ('research', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.research')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Research_Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.article')),
                ('research', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.research')),
            ],
        ),
        migrations.AddField(
            model_name='research',
            name='articles',
            field=models.ManyToManyField(through='DataBase.Research_Article', to='DataBase.article'),
        ),
        migrations.AddField(
            model_name='research',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Preproc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.FloatField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.article')),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.keyword')),
                ('research', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.research')),
            ],
        ),
        migrations.AddField(
            model_name='keyword',
            name='research',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.research'),
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=1024)),
                ('pos_x', models.IntegerField()),
                ('pos_y', models.IntegerField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.article')),
                ('research', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.research')),
            ],
        ),
        migrations.CreateModel(
            name='Article_Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DataBase.author')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ManyToManyField(through='DataBase.Article_Author', to='DataBase.author'),
        ),
    ]
