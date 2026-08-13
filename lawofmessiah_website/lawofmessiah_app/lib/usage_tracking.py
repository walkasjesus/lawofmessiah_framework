"""Helpers to record daily Bible translation and page usage for the admin reports."""
import hashlib
from datetime import date

from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import F

CACHE_SOURCES = {'bible_lib_cache', 'django_cache', 'cache'}


def _user_kind_and_key(request):
    from lawofmessiah_app.models import PageVisitDaily

    user = getattr(request, 'user', None)
    if user is not None and getattr(user, 'is_authenticated', False):
        raw_key = f'user:{user.pk}'
        return PageVisitDaily.USER_AUTHENTICATED, hashlib.sha256(raw_key.encode()).hexdigest()[:32]

    session = getattr(request, 'session', None)
    session_key = getattr(session, 'session_key', '') if session is not None else ''
    if not session_key and session is not None:
        session.save()
        session_key = session.session_key or ''
    if not session_key:
        session_key = request.META.get('REMOTE_ADDR', '') + '|' + request.META.get('HTTP_USER_AGENT', '')

    secret = str(getattr(settings, 'SECRET_KEY', ''))
    raw_key = f'anon:{secret}:{session_key}'
    return PageVisitDaily.USER_ANONYMOUS, hashlib.sha256(raw_key.encode()).hexdigest()[:32]


def _increment_or_create(model, lookup, increments, defaults=None):
    create_kwargs = dict(lookup)
    create_kwargs.update(defaults or {})
    create_kwargs.update(increments)
    try:
        with transaction.atomic():
            model.objects.create(**create_kwargs)
            return
    except IntegrityError:
        pass
    model.objects.filter(**lookup).update(**{field: F(field) + value for field, value in increments.items()})


def normalize_bible_source(source):
    if source in CACHE_SOURCES:
        return 'cache'
    if source == 'api':
        return 'api'
    return None


def record_bible_usage(request, bible, source, endpoint, verse_count=1):
    from lawofmessiah_app.models import BibleTranslationUsageDaily

    normalized_source = normalize_bible_source(source)
    if normalized_source is None:
        return

    user_kind, user_key = _user_kind_and_key(request)
    bible_id = str(getattr(bible, 'id', '') or getattr(bible, 'bible_id', '') or bible).strip()[:64]
    if not bible_id:
        return

    _increment_or_create(
        BibleTranslationUsageDaily,
        lookup={
            'usage_date': date.today(),
            'bible_id': bible_id,
            'source': normalized_source,
            'endpoint': endpoint,
            'user_key': user_key,
        },
        increments={'request_count': 1, 'verse_count': verse_count},
        defaults={
            'bible_name': str(getattr(bible, 'name', '') or '')[:255],
            'bible_language': str(getattr(bible, 'language', '') or '')[:8],
            'user_kind': user_kind,
        },
    )


def record_page_visit(request, page_label=''):
    from lawofmessiah_app.models import PageVisitDaily

    user_kind, user_key = _user_kind_and_key(request)
    language_code = str(getattr(request, 'LANGUAGE_CODE', '') or '')[:8]

    _increment_or_create(
        PageVisitDaily,
        lookup={
            'usage_date': date.today(),
            'page_path': request.path[:512],
            'language_code': language_code,
            'user_key': user_key,
        },
        increments={'visit_count': 1},
        defaults={
            'page_label': str(page_label or '')[:255],
            'user_kind': user_kind,
        },
    )
