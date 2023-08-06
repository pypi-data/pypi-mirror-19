# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils import timezone
from django.utils import formats
from django.contrib.contenttypes.models import ContentType
from yamoney.signals import transaction_success


class Transaction(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('p2p-incoming', 'Перевод из кошелька'),
        ('card-incoming', 'Перевод с карты'),
    )
    CURRENCY_CHOICES = (
        ('643', 'руб.'),
    )

    notification_type = models.CharField('Тип операции', max_length=100, choices=NOTIFICATION_TYPE_CHOICES)
    operation_id = models.CharField('Идентификатор операции', max_length=255)
    amount = models.FloatField('Сумма, которая зачислена на счет получателя')
    withdraw_amount = models.FloatField('Сумма, которая списана со счета отправителя', blank=True, null=True)
    currency = models.CharField('Валюта', max_length=100, choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES[0][0])
    datetime = models.DateTimeField('Дата и время совершения перевода')
    sender = models.CharField('Номер счета отправителя', max_length=255, blank=True,
                              help_text='Только для переводов из кошелька')
    codepro = models.BooleanField('Служебное')
    label = models.CharField('Метка платежа', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'

    def __unicode__(self):
        return '%s на сумму %.2f %s от %s' % (
            self.get_notification_type_display(),
            self.withdraw_amount or 0,
            self.get_currency_display(),
            formats.date_format(timezone.localtime(self.datetime), 'DATETIME_FORMAT')
        )

    def get_related_obj(self):
        if self.label:
            obj_type_str, obj_pk = self.label.split('-')
            if obj_type_str and obj_pk:
                app_label, model_name = obj_type_str.split('.')
                try:
                    obj_type = ContentType.objects.get_by_natural_key(app_label, model_name)
                except ContentType.DoesNotExist:
                    return None
                try:
                    obj_pk = int(obj_pk)
                except ValueError:
                    return None
                try:
                    obj = obj_type.get_object_for_this_type(pk=obj_pk)
                except obj_type.DoesNotExist:
                    return None
                else:
                    return obj
        return None

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Transaction, self).save(*args, **kwargs)
        if created:
            transaction_success.send(sender=self, related_obj=self.get_related_obj())

    @staticmethod
    def generate_label(obj):
        obj_type = ContentType.objects.get_for_model(obj)
        return '%s-%s' % ('.'.join(obj_type.natural_key()), obj.pk)
