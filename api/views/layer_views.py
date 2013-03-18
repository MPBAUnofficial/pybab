from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest
from django.utils.translation import ugettext as _

from tojson import render_to_json
from pybab.models import CatalogLayer, LayerGroup

from .commons import login_required_json_default, get_subtree_for
from ..forms import ShapeForm
from ..api_settings import MAX_LAYER_UPLOADS, MAX_GROUPS
from ..modifiers import get_style, alter_id


@login_required_json_default
@render_to_json(mimetype='text/html')
def catalog_layer(request, index=0):
    user = request.user
    index = int(index)

    if request.method == 'GET':
        return get_subtree_for(user, index, LayerGroup, CatalogLayer,
                               extra_data=[get_style, alter_id, {'checked': False}])
    elif request.method == 'POST':
        return _upload_layer(request, user)
    elif request.method == 'DELETE':
        return _delete_layer(user, index)
    else:
        error_msg = u"request type \"{req_type}\"is not supported".format(req_type=request.method)
        return {'success': False,
                'message': _(error_msg)}, {'cls':HttpResponseForbidden}


def _upload_layer(request, user):
    if user.userlayerlink_set.count() > MAX_LAYER_UPLOADS:
        error_msg = u"too many layers uploaded. max number is {0}".format(MAX_LAYER_UPLOADS)
        return {'success': False,
                'message': _(error_msg)}, {'cls':HttpResponseForbidden}
    shape_form = ShapeForm(request.POST, request.FILES, user=user)
    if shape_form.is_valid():
        shape_form.save()
        return {'success': True}
    else:
        return {'success': False,
                'message': shape_form.errors}, {'cls':HttpResponseBadRequest}


def _delete_layer(user, index):
    real_id = index / MAX_GROUPS
    try:
        catalog_layer = CatalogLayer.objects.get(pk=real_id)
    except CatalogLayer.DoesNotExist:
        error_msg = _(u"layer with id '%s' does not exist") % (real_id,)
        return {'success': False,
                'message': error_msg}, {'cls':HttpResponseNotFound}

    if not catalog_layer.related_user_set.exists():
        error_msg = _(u"layer with id '%s' is public, you can not delete it.") % (real_id,)
        return {'success': False,
                'message': error_msg}, {'cls':HttpResponseForbidden}
    else:
        try:
            catalog_layer.related_user_set.get(user=user)
        except catalog_layer.related_user_set.DoesNotExist:
            error_msg = _(u"layer with id '%s' does not belong to the current user.") % (real_id,)
            return {'success': False,
                    'message': error_msg}, {'cls':HttpResponseForbidden}
        #This will also delete UserLayerLink as a result of the CASCADE trigger.
        catalog_layer.delete()
        return {'success': True}
