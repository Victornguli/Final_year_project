# Generated by Django 2.1.5 on 2019-03-31 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190323_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=50, null=True)),
                ('receiver', models.CharField(choices=[('students', 'students'), ('supervisors', 'supervisors'), ('everyone', 'everyone')], max_length=10)),
                ('document', models.FileField(upload_to='notifications/')),
            ],
        ),
    ]
