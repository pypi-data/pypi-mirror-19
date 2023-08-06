# coding: utf-8

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from django_th.tools import warn_user_and_admin


class ServicesActivated(models.Model):

    """
        Services Activated from the admin
    """
    name = models.CharField(max_length=200, unique=True)
    status = models.BooleanField(default=False)
    auth_required = models.BooleanField(default=True)
    self_hosted = models.BooleanField(default=False)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Services'
        verbose_name_plural = 'Services'

    def show(self):
        """

        :return: string representing object
        """
        return "Service Activated %s %s %s %s" % (self.name, self.status,
                                                  self.auth_required,
                                                  self.description)

    def __str__(self):
        return self.name


class UserService(models.Model):

    """
        UserService a model to link service and user
    """
    user = models.ForeignKey(User)
    token = models.CharField(max_length=255, blank=True)
    name = models.ForeignKey(
        ServicesActivated, to_field='name', related_name='+')
    username = models.CharField(
        _('username'), max_length=255, default='', blank=True)
    password = models.CharField(
        _('password'), max_length=128, default='', blank=True)
    host = models.CharField(_('host'), max_length=255, default='', blank=True)
    client_id = models.CharField(
        _('client id'), max_length=255, default='', blank=True)
    client_secret = models.CharField(
        _('client secret'), max_length=255, default='', blank=True)

    def show(self):
        """

        :return: string representing object
        """
        return "User Service %s %s %s" % (self.user, self.token, self.name)

    def __str__(self):
        return self.name.name


class TriggerService(models.Model):

    """
        TriggerService
    """
    provider = models.ForeignKey(UserService, related_name='+', blank=True)
    consumer = models.ForeignKey(UserService, related_name='+', blank=True)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True)
    date_triggered = models.DateTimeField(null=True)
    status = models.BooleanField(default=False)
    result = models.CharField(max_length=255, default='')
    date_result = models.DateTimeField(auto_now=True, null=True)
    provider_failed = models.IntegerField(db_index=True, default=0)
    consumer_failed = models.IntegerField(db_index=True, default=0)

    def show(self):
        """

        :return: string representing object
        """
        return "My Service %s - %s - %s - %s" % (self.user,
                                                 self.provider.name,
                                                 self.consumer.name,
                                                 self.description)

    def __str__(self):
        return "%s - %s - %s - %s" % (self.user,
                                      self.provider.name,
                                      self.consumer.name,
                                      self.description)


def update_result(trigger_id, msg, status):
    """
    :param trigger_id: trigger id
    :param msg: result msg
    :param status: status of the handling of the current trigger
    :return:
    """
    # if status is True, reset *_failed counter
    if status:
        TriggerService.objects.filter(id=trigger_id).update(result=msg,
                                                            date_result=now(),
                                                            provider_failed=0,
                                                            consumer_failed=0)
    # otherwise, add 1 to the consumer_failed
    else:
        service = TriggerService.objects.get(id=trigger_id)
        failed = service.consumer_failed + 1
        if failed > settings.DJANGO_TH.get('failed_tries', 5):
            TriggerService.objects.filter(id=trigger_id).\
                update(result=msg, date_result=now(), status=False)
        else:
            TriggerService.objects.filter(id=trigger_id).\
                update(result=msg, date_result=now(), consumer_failed=failed)

        warn_user_and_admin('consumer', service)
