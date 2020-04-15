# Generated by Django 3.0.4 on 2020-04-15 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facilities', '0001_initial'),
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignGroupCubic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now_add=True, null=True)),
                ('assigned_business_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='custom_user.BusinessGroup')),
                ('assigner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('cubic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilities.Cubic')),
            ],
            options={
                'unique_together': {('cubic', 'assigned_business_group')},
            },
        ),
    ]
