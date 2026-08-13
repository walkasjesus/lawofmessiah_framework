from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandments_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BibleTranslationUsageDaily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_date', models.DateField(db_index=True)),
                ('bible_id', models.CharField(db_index=True, max_length=64)),
                ('bible_name', models.CharField(blank=True, default='', max_length=255)),
                ('bible_language', models.CharField(blank=True, default='', max_length=8)),
                ('source', models.CharField(choices=[('api', 'API'), ('cache', 'Cache'), ('blocked', 'Blocked')], db_index=True, max_length=16)),
                ('endpoint', models.CharField(choices=[('study_page', 'Bible Study page'), ('verses_api', 'Bible Study verses API'), ('search_api', 'Bible Study search API'), ('commandment_verses', 'Commandment verses API'), ('lesson_verses', 'Lesson verses API'), ('law_of_messiah_verses', 'Law of Messiah verses API'), ('maimonides_verses', 'Maimonides verses API')], db_index=True, max_length=32)),
                ('user_kind', models.CharField(choices=[('authenticated', 'Authenticated'), ('anonymous', 'Anonymous')], db_index=True, max_length=16)),
                ('user_key', models.CharField(db_index=True, max_length=64)),
                ('request_count', models.PositiveIntegerField(default=0)),
                ('verse_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-usage_date', 'bible_id', 'source', 'endpoint'],
                'verbose_name': 'Bible usage report',
                'verbose_name_plural': 'Bible Usage Report',
            },
        ),
        migrations.CreateModel(
            name='PageVisitDaily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_date', models.DateField(db_index=True)),
                ('page_path', models.CharField(db_index=True, max_length=512)),
                ('page_label', models.CharField(blank=True, default='', max_length=255)),
                ('language_code', models.CharField(blank=True, default='', max_length=8)),
                ('user_kind', models.CharField(choices=[('authenticated', 'Authenticated'), ('anonymous', 'Anonymous')], db_index=True, max_length=16)),
                ('user_key', models.CharField(db_index=True, max_length=64)),
                ('visit_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-usage_date', 'page_path', 'language_code'],
                'verbose_name': 'Page usage report',
                'verbose_name_plural': 'Page Usage Report',
            },
        ),
        migrations.AddConstraint(
            model_name='bibletranslationusagedaily',
            constraint=models.UniqueConstraint(fields=('usage_date', 'bible_id', 'source', 'endpoint', 'user_key'), name='uniq_bible_usage_daily_bucket'),
        ),
        migrations.AddConstraint(
            model_name='pagevisitdaily',
            constraint=models.UniqueConstraint(fields=('usage_date', 'page_path', 'language_code', 'user_key'), name='uniq_page_visit_daily_bucket'),
        ),
        migrations.AddIndex(
            model_name='bibletranslationusagedaily',
            index=models.Index(fields=['usage_date', 'bible_id'], name='commandments_app_bible_usage_daily_idx'),
        ),
        migrations.AddIndex(
            model_name='bibletranslationusagedaily',
            index=models.Index(fields=['usage_date', 'source'], name='commandments_app_bible_usage_source_idx'),
        ),
        migrations.AddIndex(
            model_name='bibletranslationusagedaily',
            index=models.Index(fields=['bible_id', 'user_key'], name='commandments_app_bible_usage_user_idx'),
        ),
        migrations.AddIndex(
            model_name='pagevisitdaily',
            index=models.Index(fields=['usage_date', 'page_path'], name='commandments_app_page_visit_date_path_idx'),
        ),
        migrations.AddIndex(
            model_name='pagevisitdaily',
            index=models.Index(fields=['usage_date', 'language_code'], name='commandments_app_page_visit_date_lang_idx'),
        ),
        migrations.AddIndex(
            model_name='pagevisitdaily',
            index=models.Index(fields=['page_path', 'user_key'], name='commandments_app_page_visit_path_user_idx'),
        ),
    ]
