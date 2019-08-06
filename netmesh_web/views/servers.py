from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages as alerts
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from netmesh_web.forms import SearchForm

from netmesh_api.models import Server
from django import forms
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import FormActions


class ServerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout.append(Submit('save', 'Save'))
        self.helper.layout.append(HTML(
            '<a href="{}" class="btn btn-default" role="button">{}</a>'.format(
                reverse_lazy('servers', kwargs={}),
                'Cancel')
        ))

    class Meta:
        model = Server
        exclude = []


@login_required
def server_list(request, template_name='servers/list.html'):
    servers_list = Server.objects.all().order_by('-pk')
    paginator = Paginator(servers_list, 15)
    page = request.GET.get('page')
    servers = paginator.get_page(page)
    context = {
        'servers': servers
    }
    return render(request, template_name, context=context)


@login_required
def server_create(request, template_name='servers/form.html'):
    form = ServerForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        alerts.success(
            request,
            _("You've successfully created server '%s.'") % instance
        )
        return server_list(request)
    return render(request, template_name, {'form': form})