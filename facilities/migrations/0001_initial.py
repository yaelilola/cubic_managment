# Generated by Django 3.0.5 on 2020-04-11 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('floor_num', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilities.Campus')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('lab', 'lab'), ('conference_room', 'conference_room')], max_length=100)),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilities.Floor')),
            ],
        ),
        migrations.CreateModel(
            name='Cubic',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('shared', 'shared'), ('private', 'private')], max_length=100)),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilities.Space')),
            ],
        ),
        migrations.AddField(
            model_name='campus',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilities.Site'),
        ),
    ]
