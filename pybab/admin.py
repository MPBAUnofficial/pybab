from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .forms import LayerGroupForm, StatisticalGroupForm
from .forms import CatalogLayerForm, CatalogStatisticalForm
from .models import Element, CatalogLayer, CatalogStatistical
from .models import LayerGroup, StatisticalGroup, Style
from .models import Indicator, IndicatorGroup, IndicatorTree


class LayerChangeList(ChangeList):
    def results(self):
        return LayerGroup.objects.tree_sorted_levels()


class LayerGroupAdmin(admin.ModelAdmin):
    form = LayerGroupForm

    def get_changelist(self,request, **kwargs):
        return LayerChangeList

    def get_form(self, request, obj=None, **kwargs):
        form = super(LayerGroupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent'].choices=\
            LayerGroup.objects.subtree_sorted_indented(
                parent=LayerGroup.objects.get(id=LayerGroup.ROOT_ID),
                to_exclude=(obj,)
                )
        if obj and obj.parent:
            form.base_fields['parent'].initial = obj.parent.id
        return form

# class IndicatorChangeList(ChangeList):
#     def results(self):
#         return IndicatorGroup.objects.tree_sorted_levels()

# class IndicatorGroupAdmin(admin.ModelAdmin):
#     form = IndicatorGroupForm
#
#     def get_changelist(self,request, **kwargs):
#         return IndicatorChangeList
#
#     def get_form(self, request, obj=None, **kwargs):
#         form = super(IndicatorGroupAdmin, self).get_form(request, obj, **kwargs)
#         form.base_fields['parent'].choices=\
#             IndicatorGroup.objects.subtree_sorted_indented(
#                 parent=IndicatorGroup.objects.get(id=IndicatorGroup.ROOT_ID),
#                 to_exclude=(obj,)
#                 )
#         if obj and obj.parent:
#             form.base_fields['parent'].initial = obj.parent.id
#         return form


class StatisticalChangeList(ChangeList):
    def results(self):
        return StatisticalGroup.objects.tree_sorted_levels()


class StatisticalGroupAdmin(admin.ModelAdmin):
    form = StatisticalGroupForm

    def get_changelist(self,request, **kwargs):
        return StatisticalChangeList

    def get_form(self, request, obj=None, **kwargs):
        form = super(StatisticalGroupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent'].choices=\
            StatisticalGroup.objects.subtree_sorted_indented(
                parent=StatisticalGroup.objects.get(id=StatisticalGroup.ROOT_ID),
                to_exclude=(obj,)
                )
        if obj and obj.parent:
            form.base_fields['parent'].initial = obj.parent.id
        return form


def catalog_and_group(obj):
    return u"%s <span style='margin-left: 30%%;left:0px;position:absolute;'>Path: %s</span>" % (obj, obj.group.path)

catalog_and_group.allow_tags = True
catalog_and_group.short_description = "CatalogLayer"


class CatalogChangeList(ChangeList):
    def get_query_set(self, request):
        queryset = super(CatalogChangeList, self).get_query_set(request)
        return queryset.order_by("group__pk")


class CatalogLayerAdmin(admin.ModelAdmin):
    form = CatalogLayerForm
    list_display = (catalog_and_group, )

    def get_changelist(self, request, **kwargs):
        return CatalogChangeList

    def get_form(self, request, obj=None, **kwargs):
        form = super(CatalogLayerAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['group'].choices = \
            LayerGroup.objects.subtree_sorted_indented(parent=LayerGroup.objects.get(id=LayerGroup.ROOT_ID),)
        if obj:
            form.base_fields['group'].initial = obj.group.id
        return form


class CatalogStatisticalAdmin(admin.ModelAdmin):
    form = CatalogStatisticalForm
    list_display = (catalog_and_group, )

    def get_changelist(self,request, **kwargs):
        return CatalogChangeList

    def get_form(self, request, obj=None, **kwargs):
        form = super(CatalogStatisticalAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['group'].choices = \
            StatisticalGroup.objects.subtree_sorted_indented(parent=StatisticalGroup.objects.get(id=StatisticalGroup.ROOT_ID),)
        if obj:
            form.base_fields['group'].initial = obj.group.id
        return form

# class CatalogIndicatorAdmin(admin.ModelAdmin):
#     form = CatalogIndicatorForm
#
#     def get_form(self, request, obj=None, **kwargs):
#         form = super(CatalogIndicatorAdmin, self).get_form(request, obj, **kwargs)
#         form.base_fields['group'].choices=\
#             IndicatorGroup.objects.subtree_sorted_indented(
#                 parent=IndicatorGroup.objects.get(id=IndicatorGroup.ROOT_ID),
#                 )
#         if obj:
#             form.base_fields['group'].initial = obj.group.id
#         return form

admin.site.register(Element)
admin.site.register(CatalogLayer, CatalogLayerAdmin)
admin.site.register(CatalogStatistical, CatalogStatisticalAdmin)
admin.site.register(LayerGroup, LayerGroupAdmin)
admin.site.register(StatisticalGroup, StatisticalGroupAdmin)
admin.site.register(Style)
admin.site.register(Indicator)
admin.site.register(IndicatorGroup)
admin.site.register(IndicatorTree)
