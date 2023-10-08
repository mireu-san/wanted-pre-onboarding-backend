# Generated by Django 4.2.6 on 2023-10-08 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("SubmitHistoryApp", "0001_initial"),
        ("UserApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="submithistory",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="UserApp.user"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="submithistory",
            unique_together={("user", "job_posting")},
        ),
    ]