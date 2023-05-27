from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin
from .models import Andraikitra, Apv, Bordereau, Fikambanana, Kristianina,\
    Lohampianakaviana, Tokantrano, Mpikambana


class AndraikitraAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('andraikitra',)
    ordering = ('id',)

    class AndraikitraResource(resources.ModelResource):
        class Meta:
            model = Andraikitra

    resource_class = AndraikitraResource


class ApvAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('apv', 'mpiaro', 'fankalazana')
    ordering = ('apv',)

    class ApvResource(resources.ModelResource):
        class Meta:
            model = Apv
            skip_unchanged = True
            report_skipped = True
            exclude = ('id',)
            import_id_fields = ('apv', 'mpiaro', 'fankalazana')

    resource_class = ApvResource

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['apv']
        return []


class BordereauAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('get_date', 'numero', 'ligne', 'lohampianakaviana',
                    'get_apv', 'get_karatra', 'taona', 'get_total', 'hasina',
                    'seminera', 'diosezy')
    search_fields = ['lohampianakaviana__kristianina__anarana', 'numero',
                     'lohampianakaviana__karatra',
                     'lohampianakaviana__kristianina__apv__apv']
    autocomplete_fields = ['lohampianakaviana']

    class BordereauResource(resources.ModelResource):
        class Meta:
            model = Bordereau
            fields = ('date', 'numero', 'ligne', 'verse_par', 'recu_par',
                      'taona', 'hasina', 'seminera', 'diosezy', 'marina',
                      'lohampianakaviana',
                      'lohampianakaviana__kristianina__anarana',
                      'lohampianakaviana__kristianina__apv__apv',
                      'lohampianakaviana__karatra',
                      'lohampianakaviana__adiresy')
            exclude = ('id',)
            import_id_fields = ('date', 'numero', 'ligne', 'verse_par',
                                'recu_par', 'taona', 'hasina', 'seminera',
                                'diosezy', 'marina', 'lohampianakaviana')
            export_order = ('date', 'numero', 'ligne',
                            'lohampianakaviana__kristianina__apv__apv',
                            'lohampianakaviana__kristianina__anarana',
                            'lohampianakaviana__karatra',
                            'lohampianakaviana__adiresy', 'verse_par',
                            'recu_par', 'taona', 'hasina', 'seminera',
                            'diosezy', 'marina')

    resource_class = BordereauResource

    @admin.display(description='date', ordering='date')
    def get_date(self, obj):
        return obj.date.strftime('%d/%m/%y')

    @admin.display(description='karatra',
                   ordering='lohampianakaviana__karatra')
    def get_karatra(self, obj):
        return obj.lohampianakaviana.karatra

    @admin.display(description='apv',
                   ordering='lohampianakaviana__kristianina__apv')
    def get_apv(self, obj):
        return obj.lohampianakaviana.kristianina.apv

    @admin.display(description='total')
    def get_total(self, obj):
        return obj.hasina + obj.seminera + obj.diosezy


class FikambananaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('sokajy', 'fikambanana', 'mpiaro', 'fankalazana')
    ordering = ('sokajy', 'fikambanana')

    class FikambananaResource(resources.ModelResource):
        class Meta:
            model = Fikambanana

    resource_class = FikambananaResource


class KristianinaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('anarana', 'apv', 'get_lohany', 'get_laharana',
                    'nahaterahana', 'nahatongavana', 'batemy', 'eokaristia',
                    'fankaherezana', 'mariazy', 'asa', 'fanamarihana')
    ordering = ['anarana']
    search_fields = ['anarana', 'apv__apv']

    class KristianinaResource(resources.ModelResource):
        class Meta:
            model = Kristianina

    resource_class = KristianinaResource

    @admin.display(description='lohany',
                   ordering='tokantrano__lohampianakaviana__'
                            'kristianina__anarana')
    def get_lohany(self, obj):
        return obj.tokantrano.lohampianakaviana.kristianina.anarana

    @admin.display(description='laharana', ordering='tokantrano__laharana')
    def get_laharana(self, obj):
        return obj.tokantrano.laharana


class LohampianakavianaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('kristianina', 'get_apv', 'karatra', 'isaina',
                    'adiresy', 'fanamarihana')
    ordering = ('kristianina__anarana', 'kristianina__apv__apv')
    search_fields = ['kristianina__anarana', 'karatra',
                     'kristianina__apv__apv']
    autocomplete_fields = ['kristianina']

    class LohampianakavianaResource(resources.ModelResource):
        class Meta:
            model = Lohampianakaviana
            fields = (
                'kristianina', 'karatra', 'isaina', 'adiresy', 'fanamarihana',
                'kristianina__anarana', 'kristianina__apv__apv'
            )
            # skip_unchanged = True
            # report_skipped = True
            exclude = ('id',)
            import_id_fields = ('kristianina', 'karatra', 'isaina', 'adiresy',
                                'fanamarihana')
            export_order = ('kristianina__anarana', 'kristianina__apv__apv',
                            'kristianina', 'karatra', 'isaina', 'adiresy',
                            'fanamarihana')

    resource_class = LohampianakavianaResource

    @admin.display(description='apv', ordering='kristianina__apv__apv')
    def get_apv(self, obj):
        return obj.kristianina.apv

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['kristianina']
        return []


class MpikambanaAdmin(admin.ModelAdmin):
    list_display = ('fikambanana', 'andraikitra', 'kristianina')
    ordering = ('fikambanana', 'andraikitra')


class TokantranoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('get_apv', 'lohampianakaviana', 'kristianina', 'laharana')
    ordering = ('kristianina__apv__apv',
                'lohampianakaviana__kristianina__anarana', 'laharana',)
    search_fields = ['kristianina__anarana', 'kristianina__apv__apv',
                     'lohampianakaviana__kristianina__anarana']
    autocomplete_fields = ['lohampianakaviana', 'kristianina']

    class TokantranoResource(resources.ModelResource):
        class Meta:
            model = Tokantrano
            fields = ('kristianina', 'lohampianakaviana', 'laharana',
                      'kristianina__apv__apv',
                      'lohampianakaviana__kristianina__anarana',
                      'lohampianakaviana__karatra',
                      'lohampianakaviana__adiresy',
                      'kristianina__anarana', 'kristianina__nahaterahana')
            # skip_unchanged = True
            # report_skipped = True
            exclude = ('id',)
            import_id_fields = ('kristianina', 'lohampianakaviana', 'laharana')
            export_order = ('kristianina__apv__apv',
                            'lohampianakaviana__kristianina__anarana',
                            'lohampianakaviana__karatra',
                            'lohampianakaviana__adiresy', 'laharana',
                            'kristianina__anarana',
                            'kristianina__nahaterahana')

    resource_class = TokantranoResource

    @admin.display(description='apv', ordering='kristianina__apv__apv')
    def get_apv(self, obj):
        return obj.kristianina.apv

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['kristianina']
        return []


admin.site.register(Andraikitra, AndraikitraAdmin)
admin.site.register(Apv, ApvAdmin)
admin.site.register(Bordereau, BordereauAdmin)
admin.site.register(Fikambanana, FikambananaAdmin)
admin.site.register(Kristianina, KristianinaAdmin)
admin.site.register(Lohampianakaviana, LohampianakavianaAdmin)
admin.site.register(Tokantrano, TokantranoAdmin)
admin.site.register(Mpikambana, MpikambanaAdmin)
