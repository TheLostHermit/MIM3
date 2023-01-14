import os, pytz
from django.core.files.storage import default_storage
from django.db.models import FileField

from datetime import datetime
from django.utils import timezone
from datetime import timezone as tz
# Adapted from file cleanup function created by Tim Kamanin at https://timonweb.com/django/cleanup-files-and-images-on-model-delete-in-django/
def file_cleanup(sender, **kwargs):
    """
    File cleanup callback used to emulate the old delete
    behavior using signals. Initially django deleted linked
    files when an object containing a File/ImageField was deleted.

    Usage:
    >>> from django.db.models.signals import post_delete
    >>> post_delete.connect(file_cleanup, sender=MyModel, dispatch_uid="mymodel.file_cleanup")
    """

    for field in sender._meta.get_fields():

        fieldname = field.name
        if field and isinstance(field, FileField):
            inst = kwargs["instance"]
            f = getattr(inst, fieldname)
            m = inst.__class__._default_manager
            if (
                hasattr(f, "path")
                and os.path.exists(f.path)
                and not m.filter(
                    **{"%s__exact" % fieldname: getattr(inst, fieldname)}
                ).exclude(pk=inst._get_pk_val())
            ):
                try:
                    default_storage.delete(f.path)
                except:
                    pass

# makes the inputs of forms timezone aware and converts them from local time to UTC to maintain database uniformity
def apply_tz_offset(date, time):

    # for some reason there is discrepancy between this time converted to UTC and the inputted time
    # (eg: time inputted from Americas/St. Lucia gets 24 minutes added to it). This might be part of daylight savings
    if date and time:
        this_datetime = datetime.combine(date, time)
        std_time = this_datetime.astimezone(tz.utc)
        print(std_time.date(), std_time.time())
        return std_time