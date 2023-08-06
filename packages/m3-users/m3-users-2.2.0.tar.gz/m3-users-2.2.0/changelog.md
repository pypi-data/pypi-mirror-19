## История изменений

**2.2.0**
- Добавлены миграции django 1.8
- Функция ``patterns`` из ``django.conf.urls.defaults`` заменена на
  одноименную из ``django.conf.urls``.
- Декоратор ``django.transaction.commit_on_success`` заменен на
  ``m3_django_compat.atomic``.
- Добавил поддержку кастомных моделей пользователя.

**2.1.1**
- Изменил MANIFEST.in. Добавлен m3-builder, .gitignore, REQUIREMENTS, changelog
