# Generated by Django 3.0.4 on 2020-04-15 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('focal_point', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
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
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilities.Building')),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('Regular', 'Regular'), ('Lab', 'Lab'), ('Conference Room', 'Conference Room')], max_length=100)),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilities.Floor')),
            ],
        ),
        migrations.CreateModel(
            name='Cubic',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('shared', 'shared'), ('private', 'private')], max_length=100)),
                ('area', models.DecimalField(decimal_places=5, max_digits=10)),
                ('focal_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='focal_point.FocalPoint')),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilities.Space')),
            ],
        ),
        migrations.AddField(
            model_name='building',
            name='campus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilities.Campus'),
        ),
    ]
