# Generated by Django 2.1.5 on 2022-05-12 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_file', models.FileField(upload_to='default')),
                ('description', models.CharField(max_length=200)),
                ('short_desc', models.CharField(default='NULL Desc', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UploadTrain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_file', models.FileField(blank=True, upload_to='uploads')),
                ('default_training_file', models.CharField(blank=True, max_length=200)),
                ('test_file', models.FileField(upload_to='uploads')),
                ('training_model', models.CharField(choices=[('simple', 'Unigram/Bigram Scores'), ('complex', 'RNN Model')], max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UploadWithDefault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_file', models.CharField(max_length=200)),
                ('test_file', models.FileField(upload_to='uploads')),
                ('training_model', models.CharField(choices=[('unigram', 'Unigram Probability'), ('bigram', 'Bigram Probability'), ('posUnigram', 'Positional Unigram Score'), ('posBigram', 'Positional Bigram Score')], max_length=128)),
            ],
        ),
    ]
