# -*- coding: utf-8 -*-

from sendfile import sendfile

from django.views.generic import View, TemplateView
from django.core import signing
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.http import HttpResponseForbidden

from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from datadownloader.models import Dump

signer = signing.Signer(salt='datadownloader')


class MainView(TemplateView):
    template_name = "admin/datadownloader/index.html"

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kw):
        return super(MainView, self).dispatch(*args, **kw)

    def get_context_data(self, **kwargs):
        context = super(MainView,
                        self).get_context_data(**kwargs)

        context['token'] = signer.sign(get_random_string())
        context['metadata'] = {}
        for section in ["db", "media", "data"]:
            dump = Dump(section)
            context['metadata'][section] = dump.get_metadata()
        return context


class CreateArchiveView(View):
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kw):
        return super(CreateArchiveView, self).dispatch(*args, **kw)

    def get(self, request, *args, **kwargs):
        dump = Dump(kwargs['data_type'])
        dump.create()
        return redirect('datadownloader_index')


class DeleteArchiveView(View):
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kw):
        return super(DeleteArchiveView, self).dispatch(*args, **kw)

    def get(self, request, *args, **kwargs):
        dump = Dump(kwargs['data_type'])
        dump.destroy()
        return redirect('datadownloader_index')


class DownloadArchiveView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            signer.unsign(token)
        except signing.BadSignature:
            return HttpResponseForbidden()

        dump = Dump(kwargs['data_type'])
        return sendfile(request,
                        dump.path,
                        attachment=True,
                        attachment_filename=dump.archive_name,
                        mimetype=dump.mimetype)
