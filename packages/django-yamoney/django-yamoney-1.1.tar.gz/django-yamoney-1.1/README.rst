=====
Yamoney
=====

Django приложение для приема денег на кошелек Yandex.Money

Установка
-----------

1. Добавить "yamoney" в ваш INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'yamoney',
    )

2. Добавить yamoney URLconf в urls.py вашего проекта::

    url(r'^yamoney/', include('yamoney.urls'))

3. Создать форму оплаты с помощью yamoney.forms.paymentform_factory::

    payment_form = paymentform_factory(
        u'Оплата участия',  # описание платежа
        2000,               # сумма
        event               # объект модели
    )

4. Слушать yamoney.signals.transaction_success сигнал, где sender - транзакция, related_obj - объект модели.

