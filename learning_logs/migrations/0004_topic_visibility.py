# Generated by Django 4.0.4 on 2022-07-06 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0003_topic_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='visibility',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='private', max_length=7),
        ),
    ]