import locale

from django.db.models import get_model
from django.http import HttpResponse
from django.utils import simplejson

from smart_selects.utils import unicode_sorter


def chainchain(request, app, model, field, models, value, manager=None):
    Models = models.split('.')
    Fields = field.split('.')
    if len(Models) != len(Fields):
        return HttpResponse('Model and field list need to be same length', status=500)
    for c in zip(Models,Fields):
        Model = get_model(app,c[0])
        object = Model.objects.get(pk=value)
        value = getattr(object,c[1])
        if hasattr(value, 'pk'):
            value = value.pk
    result = []
    for item in value.all():
        result.append({'value':item.pk, 'display':unicode(item)})
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')

def filterchain(request, app, model, field, value, manager=None):
    Model = get_model(app, model)
    if value == '0':
        keywords = {str("%s__isnull" % field):True}
    else:
        keywords = {str(field): str(value)}
    if manager is not None and hasattr(Model, manager):
        queryset = getattr(Model, manager).all()
    else:
        queryset = Model.objects
    results = list(queryset.filter(**keywords))
    results.sort(cmp=locale.strcoll, key=lambda x:unicode_sorter(unicode(x)))
    result = []
    for item in results:
        result.append({'value':item.pk, 'display':unicode(item)})
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')

def filterchain_all(request, app, model, field, value):
    Model = get_model(app, model)
    if value == '0':
        keywords = {str("%s__isnull" % field):True}
    else:
        keywords = {str(field): str(value)}
    results = list(Model.objects.filter(**keywords))
    results.sort(cmp=locale.strcoll, key=lambda x:unicode_sorter(unicode(x)))
    final = []
    for item in results:
        final.append({'value':item.pk, 'display':unicode(item)})
    results = list(Model.objects.exclude(**keywords))
    results.sort(cmp=locale.strcoll, key=lambda x:unicode_sorter(unicode(x)))
    final.append({'value':"", 'display':"---------"})

    for item in results:
        final.append({'value':item.pk, 'display':unicode(item)})
    json = simplejson.dumps(final)
    return HttpResponse(json, mimetype='application/json')
