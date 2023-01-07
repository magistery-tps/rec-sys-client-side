# Generated by Django 4.1 on 2023-01-07 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recsysweb', '0045_alter_recommender_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommenderensembleconfig',
            name='ensemble',
            field=models.ForeignKey(db_column='ensemble_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_ensemble_id', to='recsysweb.recommenderensemble', verbose_name='Recommender Ensemble'),
        ),
    ]
