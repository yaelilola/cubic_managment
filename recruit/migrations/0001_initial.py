# Generated by Django 3.0.4 on 2020-04-15 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewPosition',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('percentage', models.CharField(choices=[('full_time', 'full_time'), ('part_time', 'part_time')], max_length=100)),
                ('business_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_user.BusinessGroup')),
            ],
        ),
    ]
