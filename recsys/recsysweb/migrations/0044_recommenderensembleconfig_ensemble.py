# Generated by Django 4.1 on 2023-01-07 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recsysweb', '0043_alter_recommender_item_similarity_matrix_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommenderensembleconfig',
            name='ensemble',
            field=models.ForeignKey(db_column='recommender_ensemble_id', default=2, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_recommender_ensemble_id', to='recsysweb.recommenderensemble', verbose_name='Recommender Ensemble'),
            preserve_default=False,
        ),
    ]
