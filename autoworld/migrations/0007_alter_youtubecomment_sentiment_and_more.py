# Generated by Django 5.1.2 on 2024-10-29 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoworld', '0006_youtubevideo_youtubecomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubecomment',
            name='sentiment',
            field=models.CharField(choices=[('Positive', 'Positive'), ('Negative', 'Negative'), ('Neutral', 'Neutral')], max_length=10, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='youtubecomment',
            unique_together={('video', 'text')},
        ),
    ]
