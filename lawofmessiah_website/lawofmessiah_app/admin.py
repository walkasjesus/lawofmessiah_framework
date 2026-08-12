from django.contrib import admin
from django.db import models
from django.urls import path

from lawofmessiah_app.models import (
    LawOfMessiah,
    LawOfMessiahBibleReference,
    LawOfMessiahDrawing,
    Maimonides,
    MaimonidesBibleReference,
    Redirect,
)


class Bible(models.Model):
    class Meta:
        managed = False
        verbose_name_plural = 'Bible'
        app_label = 'commandments_app'


class BibleAdmin(admin.ModelAdmin):
    model = Bible

    def get_urls(self):
        from lawofmessiah_app.views.admin.admin_bible_view import AdminBibleView
        view_name = '{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('', AdminBibleView.as_view(), name=view_name),
        ]


class LawOfMessiahBibleReferenceInline(admin.TabularInline):
    model = LawOfMessiahBibleReference
    extra = 0


class LawOfMessiahDrawingInline(admin.TabularInline):
    model = LawOfMessiahDrawing
    extra = 0


admin.site.register(Bible, BibleAdmin)


@admin.register(LawOfMessiah)
class LawOfMessiahAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_dataset', 'commandment_type', 'is_unique', 'classical_commandment')
    search_fields = ('id', 'title', 'commandment', 'category')
    list_filter = ('source_dataset', 'commandment_type', 'is_unique', 'classical_commandment')
    inlines = (LawOfMessiahBibleReferenceInline, LawOfMessiahDrawingInline)


@admin.register(Maimonides)
class MaimonidesAdmin(admin.ModelAdmin):
    list_display = ('id', 'commandment_type')
    search_fields = ('id', 'commandment')
    list_filter = ('commandment_type',)


@admin.register(MaimonidesBibleReference)
class MaimonidesBibleReferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'maimonides', 'reference_type', 'source_code', 'book')
    search_fields = ('maimonides__id', 'source_code')
    list_filter = ('reference_type', 'book')


@admin.register(LawOfMessiahDrawing)
class LawOfMessiahDrawingAdmin(admin.ModelAdmin):
    list_display = ('id', 'law_of_messiah', 'media_type', 'title', 'target_audience', 'language', 'is_public')
    search_fields = ('title', 'description', 'law_of_messiah__id')
    list_filter = ('media_type', 'target_audience', 'language', 'is_public')


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_url')
    search_fields = ('img_url',)
