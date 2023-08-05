PyICAO9303
==========

Трансляция русских букв в латинские аналоги.
::

    >>> import pyicao9303
    >>> pyicao9303.decode('Проверка связи в 10 корпусе')
    'proverka sviazi v 10 korpuse'
    >>> pyicao9303.decode('Проверка связи в 10 корпусе', False)
    'Proverka sviazi v 10 korpuse'


TODO
----

- Добавить поддержку других стран
- Добавить обратную трансляцию
