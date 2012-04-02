from django.db.models import get_model
from django.http import HttpResponse
from django.utils import simplejson
import locale
from smart_selects.utils import unicode_sorter

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
    print keywords
    results = list(queryset.filter(**keywords))
    results.sort(cmp=locale.strcoll, key=lambda x:unicode_sorter(unicode(x)))
    result = []
    for item in results:
        result.append({'value':item.pk, 'display':unicode(item)})
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')

def filtersubchain(request, app, model, field, submodel, subfield, value, manager=None):
	Model = get_model(app,model)
	SubModel = get_model(app,submodel)
	subobj = SubModel.objects.get(pk=value)
	if manager is not None and hasattr(Model, manager):
		queryset = getattr(Model, manager).all()
	else:
		queryset = Model.objects
	lastobj = getattr(subobj,subfield)
	if value == '0':
		keywords = {str("%s__isnull" % field):True}
	else:
		keywords = {str(field): str(lastobj.pk)}
	results = list(queryset.filter(**keywords))
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
