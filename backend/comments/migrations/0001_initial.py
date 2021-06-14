# Generated by Django 3.1.4 on 2021-06-14 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('markers', '0004_auto_20210614_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_addr', models.GenericIPAddressField(verbose_name='IP Адрес')),
                ('email', models.EmailField(max_length=254, verbose_name='E-Mail')),
                ('text', models.TextField(max_length=400, verbose_name='Коментарий')),
                ('send_date', models.DateTimeField(verbose_name='Время отправки')),
                ('panorama', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='markers.picture')),
            ],
        ),
    ]