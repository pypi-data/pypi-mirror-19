from django.conf import settings
from django.contrib.admin import site
from django.template.defaulttags import register
from django.utils.module_loading import autodiscover_modules
from django.template import loader
from django.template.context import BaseContext


__author__ = 'hakim'


def autodiscover():
    autodiscover_modules('box', register_to=site)


@register.inclusion_tag('box_base.html', takes_context=True)
def box(context, box_name, *args, **kwargs):
    try:
        module_path = settings.BOX_MODULE_PATH + '.'

        mod = __import__(module_path + box_name, fromlist=['*'])
        obj = getattr(mod, box_name)

        if 'include_context' in kwargs and kwargs['include_context'] is True:
            obj.context['parent_context'] = context
            obj.context['include_context'] = True
        else:
            kwargs['include_context'] = False

        obj.context['args'] = kwargs

        return {'obj': obj}
    except Exception as e:
        raise


class Box(object):
    template_path = settings.BOX_TEMPLATE_PATH
    template_name = 'box_base.html'
    context = {}

    def __init__(self, *args, **kwargs):
        if self.template_name != 'box_base.html':
            self.template_name = self.template_path+'/'+self.template_name

        self.template = loader.get_template(self.template_name)

    def result(self):
        return self.template.render(BaseContext(self.context))

    def get_context(self):
        if 'include_context' in self.context and self.context['include_context']:
            return self.context['parent_context']

    def get_argument(self, key):
        if key in self.context['args']:
            return self.context['args'][key]
        else:
            return False
