# Generated by Django 3.1.6 on 2021-02-09 05:56

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
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pre_bp_sys', models.IntegerField()),
                ('pre_bp_dia', models.IntegerField()),
                ('pre_weight', models.IntegerField()),
                ('post_bp_sys', models.IntegerField()),
                ('post_bp_dia', models.IntegerField()),
                ('post_weight', models.IntegerField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]