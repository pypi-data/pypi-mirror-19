from __future__ import unicode_literals

import pytz

from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Instance
from .widgets import OpenStackTagsWidget


class BackupScheduleForm(ModelForm):
    def clean_timezone(self):
        tz = self.cleaned_data['timezone']
        if tz not in pytz.all_timezones:
            raise ValidationError('Invalid timezone', code='invalid')

        return self.cleaned_data['timezone']


class InstanceForm(ModelForm):
    class Meta:
        model = Instance
        exclude = 'uuid',
        widgets = {
            'tags': OpenStackTagsWidget(),
        }

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        for tag in 'os', 'application', 'support':
            opts = self.data.getlist("tags_%s" % tag)
            if opts[1]:
                tags.append(':'.join(opts))

        remote = self.data.get('tags_remote_type')
        if remote:
            tags.append(':'.join([remote, self.data.get('tags_remote_instance')]))

        return tags
