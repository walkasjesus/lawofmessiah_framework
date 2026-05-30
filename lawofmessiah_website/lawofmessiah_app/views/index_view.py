from django.conf import settings
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views import View

from lawofmessiah_app.models import LawOfMessiah
from lawofmessiah_app.views.law_of_messiah_view import (
    _extract_ncla_codes,
    _find_primary_drawing,
    _ncla_filter_options,
    _ncla_group_options,
    _ncla_label_map,
    _ncla_person_codes,
    _ncla_summary,
    _normalize_image_url,
    _normalize_search_text,
    _person_label_map,
    _matches_ncla_filters,
)


class IndexView(View):
    def get(self, request):
        search_query = request.GET.get('q', '').strip()
        source_dataset = request.GET.get('source_dataset', '').strip().lower()
        commandment_type_param = request.GET.get('commandment_type')
        unique_filter_param = request.GET.get('is_unique')
        default_commandment_type = '' if search_query else LawOfMessiah.COMMANDMENT_TYPE_POSITIVE
        default_unique_filter = '' if search_query else 'true'
        commandment_type = (
            commandment_type_param.strip().lower()
            if commandment_type_param is not None
            else default_commandment_type
        )
        unique_filter = (
            unique_filter_param.strip().lower()
            if unique_filter_param is not None
            else default_unique_filter
        )
        classical_filter = request.GET.get('classical_commandment', '').strip().lower()
        illustration_filter = request.GET.get('illustration', '').strip().lower()
        category = request.GET.get('category', '').strip()
        person_code = request.GET.get('ncla_person', '').strip().upper()
        application_code = request.GET.get('ncla_application', '').strip().lower()
        ncla_group = request.GET.get('ncla_group', '').strip()

        if commandment_type not in {
            LawOfMessiah.COMMANDMENT_TYPE_POSITIVE,
            LawOfMessiah.COMMANDMENT_TYPE_NEGATIVE,
            LawOfMessiah.COMMANDMENT_TYPE_BOTH,
            '',
        }:
            commandment_type = LawOfMessiah.COMMANDMENT_TYPE_POSITIVE

        if illustration_filter not in {'', 'true', 'false'}:
            illustration_filter = ''

        laws_query = LawOfMessiah.objects.order_by('id').prefetch_related('media')
        if unique_filter == 'true':
            laws_query = laws_query.filter(is_unique=True)
        elif unique_filter == 'false':
            laws_query = laws_query.filter(is_unique=False)

        if commandment_type in {
            LawOfMessiah.COMMANDMENT_TYPE_POSITIVE,
            LawOfMessiah.COMMANDMENT_TYPE_NEGATIVE,
            LawOfMessiah.COMMANDMENT_TYPE_BOTH,
        }:
            laws_query = laws_query.filter(commandment_type=commandment_type)

        if source_dataset in {LawOfMessiah.SOURCE_DATASET_OT, LawOfMessiah.SOURCE_DATASET_NT}:
            laws_query = laws_query.filter(source_dataset=source_dataset)
        if classical_filter == 'true':
            laws_query = laws_query.filter(classical_commandment=True)
        elif classical_filter == 'false':
            laws_query = laws_query.filter(classical_commandment=False)
        if category:
            laws_query = laws_query.filter(category=category)

        laws = list(laws_query)
        if illustration_filter in {'true', 'false'}:
            wants_illustration = illustration_filter == 'true'
            laws = [law for law in laws if bool(_find_primary_drawing(law)) is wants_illustration]

        if person_code or application_code or ncla_group:
            laws = [law for law in laws if _matches_ncla_filters(law, person_code, application_code, ncla_group)]

        normalized_search = _normalize_search_text(search_query)
        if normalized_search:
            search_terms = [term for term in normalized_search.split() if term]

            def _matches_search(law_obj):
                haystack = [
                    law_obj.id,
                    law_obj.title,
                    law_obj.commandment,
                    law_obj.category,
                    law_obj.translated_title,
                    law_obj.translated_commandment,
                    law_obj.translated_category,
                ]
                searchable_text = ' '.join(_normalize_search_text(item) for item in haystack if item)
                if normalized_search in searchable_text:
                    return True
                if len(search_terms) > 1:
                    return any(term in searchable_text for term in search_terms)
                return False

            laws = [law for law in laws if _matches_search(law)]

        ncla_labels = _ncla_label_map()
        for law in laws:
            law.primary_drawing = _find_primary_drawing(law)
            law.primary_drawing_url = _normalize_image_url(law.primary_drawing.img_url) if law.primary_drawing else ''
            law.ncla_human = [ncla_labels.get(code, code) for code in _extract_ncla_codes(law.ncla or [])]
            law.ncla_summary = _ncla_summary(law.ncla or [])
            law.ncla_person_icons = [
                {
                    'code': code,
                    'label': {
                        'JEW': 'Jewish',
                        'MESSIANIC': "K'rov Yisrael",
                        'GENTILE': 'Gentile',
                    }.get(code, code)
                }
                for code in _ncla_person_codes(law.ncla or [])
            ]

        filter_options = _ncla_filter_options()
        ncla_group_options = _ncla_group_options(commandment_type=commandment_type, unique_filter=unique_filter)
        category_values = list(
            LawOfMessiah.objects.exclude(category='').order_by('category').values_list('category', flat=True).distinct()
        )
        category_options = [
            {
                'value': value,
                'label': _(value),
            }
            for value in category_values
        ]

        return render(
            request,
            'pages/index.html',
            {
                'languages_total': len(settings.LANGUAGES),
                'laws': laws,
                'laws_count': len(laws),
                'selected_q': search_query,
                'selected_source_dataset': source_dataset,
                'selected_commandment_type': commandment_type,
                'selected_is_unique': unique_filter,
                'selected_classical_commandment': classical_filter,
                'selected_illustration': illustration_filter,
                'selected_category': category,
                'selected_ncla_person': person_code,
                'selected_ncla_application': application_code,
                'selected_ncla_group': ncla_group,
                'category_options': category_options,
                'ncla_person_options': filter_options['person'],
                'ncla_application_options': filter_options['application'],
                'ncla_group_options': ncla_group_options,
            },
        )
