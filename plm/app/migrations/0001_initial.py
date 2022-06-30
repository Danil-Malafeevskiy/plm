

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Unique_number', models.IntegerField(unique=True)),
                ('name_tap', models.CharField(blank=True, default='-', max_length=50)),
                ('number_support', models.IntegerField(unique=True)),
                ('VL', models.CharField(default='-', max_length=100)),
                ('type_support', models.CharField(max_length=50)),
                ('code_support', models.CharField(blank=True, default='Не определен', max_length=50)),
                ('material', models.CharField(max_length=50)),
                ('corner', models.FloatField()),
                ('X', models.FloatField()),
                ('Y', models.FloatField()),
                ('Z', models.FloatField()),
                ('shirota', models.FloatField()),
                ('dolgota', models.FloatField()),
                ('height', models.FloatField()),
                ('TPV_photo', models.CharField(blank=True, default='-', max_length=50)),
                ('UF_photo', models.CharField(blank=True, default='-', max_length=50)),
                ('photo', models.CharField(blank=True, default='-', max_length=50)),
                ('v_defects', models.CharField(blank=True, default='-', max_length=10000)),
                ('u_defects', models.CharField(blank=True, default='-', max_length=100)),
                ('code_support_in_1C', models.CharField(blank=True, default='-', max_length=200)),
                ('guid', models.IntegerField(blank=True, default=0)),
                ('flag_defects', models.BooleanField()),
                ('comment_in_TOiR', models.CharField(blank=True, default='-', max_length=100)),
                ('geometry', models.CharField(blank=True, default='-', max_length=100)),
            ],
        ),
    ]
