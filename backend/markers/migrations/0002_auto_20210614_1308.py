# Generated by Django 3.2.4 on 2021-06-14 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('markers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='picture',
            new_name='image',
        ),
        migrations.AlterField(
            model_name='marker',
            name='picture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='markers.picture', verbose_name='Отображается на изображении'),
        ),
        migrations.AlterField(
            model_name='marker',
            name='to',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='from_marker', to='markers.picture', verbose_name='Направляет на'),
        ),
    ]
