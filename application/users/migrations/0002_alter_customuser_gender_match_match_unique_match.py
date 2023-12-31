# Generated by Django 4.2.2 on 2023-07-01 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('M', 'Мужчина'), ('F', 'Женщина')], max_length=1, verbose_name='пол'),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='созданно')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='изменено')),
                ('is_sympathy', models.CharField(choices=[('NA', 'Нет ответа'), ('OK', 'Взаимно!'), ('NO', 'Не взаимно')], default='NA', max_length=2, verbose_name='взаимная симпатия')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL, verbose_name='получатель')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='отправитель')),
            ],
            options={
                'verbose_name': 'взаимная симпатия',
                'verbose_name_plural': 'взаимные симпатии',
            },
        ),
        migrations.AddConstraint(
            model_name='match',
            constraint=models.UniqueConstraint(fields=('sender', 'receiver'), name='unique_match'),
        ),
    ]
