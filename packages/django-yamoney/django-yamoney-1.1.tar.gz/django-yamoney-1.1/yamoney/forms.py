# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from hashlib import sha1
from django.db import models
from django import forms
from .conf import settings
from .models import Transaction
from .fields import DateTimeISO6801Field


class YandexPaymentForm(forms.Form):
    ACTION_URL = 'https://money.yandex.ru/quickpay/confirm.xml'
    QUICKPAY_CHOICES = (
        ('shop', 'shop'),
        ('donate', 'donate'),
        ('small', 'small'),
    )
    PAYMENTTYPE_CHOICES = (
        ('PC', 'оплата со счета Яндекс.Денег'),
        ('AC', 'оплата с банковской карты')
    )
    FIELD_NAME_MAPPING = {
        'shortDest': 'short-dest',
        'quickpayForm': 'quickpay-form',
    }
    receiver = forms.CharField(widget=forms.HiddenInput)
    formcomment = forms.CharField(max_length=50, widget=forms.HiddenInput)
    shortDest = forms.CharField(max_length=50, widget=forms.HiddenInput)
    quickpayForm = forms.ChoiceField(choices=QUICKPAY_CHOICES, initial='shop', widget=forms.HiddenInput)
    targets = forms.CharField(max_length=150, widget=forms.HiddenInput)
    sum = forms.FloatField(widget=forms.HiddenInput)
    paymentType = forms.ChoiceField(label='Варианты оплаты', choices=PAYMENTTYPE_CHOICES,
                                    initial='AC',
                                    widget=forms.RadioSelect)
    label = forms.CharField(required=False, widget=forms.HiddenInput)

    # comment = forms.CharField(required=False, max_length=200, widget=forms.HiddenInput)

    def add_prefix(self, field_name):
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(YandexPaymentForm, self).add_prefix(field_name)


class YandexNotificationForm(forms.ModelForm):
    datetime = DateTimeISO6801Field()
    sha1_hash = forms.CharField()

    class Meta:
        model = Transaction
        fields = '__all__'

    def make_hash(self):
        cd = self.data
        return sha1('&'.join(map(str, (
            cd.get('notification_type', ''),
            cd.get('operation_id', ''),
            cd.get('amount', ''),
            cd.get('currency', ''),
            cd.get('datetime', ''),
            cd.get('sender', ''),
            cd.get('codepro', ''),
            settings.YAMONEY_NOTIFICATION_SECRET,
            cd.get('label', ''),
        )))).hexdigest()

    def clean(self):
        cd = super(YandexNotificationForm, self).clean()
        sha1_hash = cd.get('sha1_hash')
        if sha1_hash != self.make_hash():
            raise forms.ValidationError('Хэш не совпадает')
        return cd


def paymentform_factory(targets, sum, label):
    if isinstance(label, models.Model):
        label = Transaction.generate_label(label)
    initial = {
        'receiver': settings.YAMONEY_ACCOUNT,
        'formcomment': settings.YAMONEY_FORM_COMMENT or targets,
        'shortDest': targets,
        'targets': targets,
        'sum': sum,
        'label': label,
    }
    return YandexPaymentForm(initial=initial)
