# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('notification_type', 'withdraw_amount', 'amount', 'currency', 'datetime',)

    def has_add_permission(self, request):
        return False


admin.site.register(Transaction, TransactionAdmin)
