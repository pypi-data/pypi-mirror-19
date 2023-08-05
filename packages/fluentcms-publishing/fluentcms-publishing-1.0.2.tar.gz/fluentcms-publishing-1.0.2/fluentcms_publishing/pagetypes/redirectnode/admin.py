from django.contrib import admin
from django.contrib.admin.options import get_ul_class
from django.contrib.admin.widgets import AdminRadioSelect
from django.utils.translation import ugettext_lazy as _

from fluent_pages.admin import PageAdmin

from fluentcms_publishing.admin import PublishingAdmin


class RedirectNodeAdmin(PageAdmin, PublishingAdmin):
    FIELDSET_REDIRECT = (_('Redirect settings'), {
        'fields': ('new_url', 'redirect_type'),
    })

    # Exclude in_sitemap
    base_fieldsets = (
        PageAdmin.FIELDSET_GENERAL,
        FIELDSET_REDIRECT,
        PageAdmin.FIELDSET_MENU,
        PageAdmin.FIELDSET_PUBLICATION,
    )

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a database Field that has declared choices.
        """
        # If the field is named as a radio_field, use a RadioSelect
        if db_field.name == 'redirect_type':
            kwargs['widget'] = AdminRadioSelect(attrs={'class': get_ul_class(admin.VERTICAL)})
        return db_field.formfield(**kwargs)
