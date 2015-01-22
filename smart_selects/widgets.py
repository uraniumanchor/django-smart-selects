import django
from django.conf import settings
from django.forms.widgets import Select
from django.core.urlresolvers import reverse
from django.utils.encoding import iri_to_uri
from django.utils.safestring import mark_safe
from django.db.models import get_model
import locale
from smart_selects.utils import unicode_sorter


if django.VERSION >= (1, 2, 0) and getattr(settings,
        'USE_DJANGO_JQUERY', True):
    USE_DJANGO_JQUERY = True
else:
    USE_DJANGO_JQUERY = False
    JQUERY_URL = getattr(settings, 'JQUERY_URL', 'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js')


class ChainedSelect(Select):
    def __init__(self, app_name, model_name, chain_field, model_field, show_all, auto_choose, manager=None, chained_model=None, *args, **kwargs):
        self.app_name = app_name
        self.model_name = model_name
        self.chain_field = chain_field
        self.model_field = model_field
        self.show_all = show_all
        self.auto_choose = auto_choose
        self.manager = manager
        self.chained_model = chained_model
        super(Select, self).__init__(*args, **kwargs)

    class Media:
        if USE_DJANGO_JQUERY:
            js = [''.join(('admin/', i)) for i in
                    ('js/jquery.min.js', 'js/jquery.init.js')] + ['js/smartselect.js']
        elif JQUERY_URL:
            js = (
                JQUERY_URL,
                'js/autocomplete.js'
            )
        else:
            js = ['js/autocomplete.js']

    def render(self, name, value, attrs=None, choices=()):
        if len(name.split('-')) > 1: # formset
            chain_field = '-'.join(name.split('-')[:-1] + [self.chain_field])
        else:
            chain_field = self.chain_field

        kwargs = {'app':self.app_name, 'model':self.model_name, 'field':self.model_field, 'value':"1"}
        if self.chained_model:
            view_name = "chained_chain"
            kwargs.update({'models':self.chained_model})
        elif self.show_all:
            view_name = "chained_filter_all"
        else:
            view_name = "chained_filter"
        if self.manager is not None:
            kwargs.update({'manager': self.manager})
        url = "/".join(reverse(view_name, kwargs=kwargs).split("/")[:-2])
        if self.auto_choose:
            auto_choose = 'true'
        else:
            auto_choose = 'false'
        empty_label = iter(self.choices).next()[1] # Hacky way to getting the correct empty_label from the field instead of a hardcoded '--------'
        final_choices = []

        if value:
            item = self.queryset.filter(pk=value)[0]
            try:
                pk = getattr(item, self.model_field + "_id")
                filter = {self.model_field:pk}
            except AttributeError:
                try: # maybe m2m?
                    pks = getattr(item, self.model_field).all().values_list('pk', flat=True)
                    filter = {self.model_field + "__in":pks}
                except AttributeError:
                    try: # maybe a set?
                        pks = getattr(item, self.model_field + "_set").all().values_list('pk', flat=True)
                        filter = {self.model_field + "__in":pks}
                    except: # give up
                        filter = {}
            filtered = list(get_model(self.app_name, self.model_name).objects.filter(**filter).distinct())
            filtered.sort(cmp=locale.strcoll, key=lambda x:unicode_sorter(unicode(x)))
            for choice in filtered:
                final_choices.append((choice.pk, unicode(choice)))
        if len(final_choices) > 1:
            final_choices = [("", (empty_label))] + final_choices
        if self.show_all:
            final_choices.append(("", (empty_label)))
            self.choices = list(self.choices)
            self.choices.sort(cmp=locale.strcoll, key=lambda x:unicode_sorter(x[1]))
            for ch in self.choices:
                if not ch in final_choices:
                    final_choices.append(ch)
        self.choices = ()
        final_attrs = self.build_attrs(attrs, name=name)
        if 'class' in final_attrs:
            final_attrs['class'] += ' chained'
        else:
            final_attrs['class'] = 'chained'
        output = super(ChainedSelect, self).render(name, value, final_attrs, choices=final_choices)
        output += "<script>generateSmartSelect(jQuery || django.jQuery, '{chain_field}', '{url}', '{id}', '{value}', {auto_choose}, '{empty_label}');</script>".format(
			chain_field=chain_field,url=url,id=attrs['id'],value=value,auto_choose=auto_choose,empty_label=empty_label)
        return mark_safe(output)
