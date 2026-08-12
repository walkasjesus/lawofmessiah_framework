from lawofmessiah_app.models.law_of_messiah import LawOfMessiahBibleReference


class BibleReferences:
    """Compatibility wrapper used by the Bible admin and cache tooling.

    The Law of Messiah app stores its scripture references in
    LawOfMessiahBibleReference rows rather than the Walkasjesus-specific model set.
    The admin and cache commands expect a uniform BibleReferences interface with
    primary(), direct(), and indirect() methods returning reference querysets.
    """

    def __init__(self):
        self.bible = None

    def primary(self):
        return self._query_references(LawOfMessiahBibleReference.objects.all())

    def direct(self):
        return self._query_references(LawOfMessiahBibleReference.objects.none())

    def indirect(self):
        return self._query_references(LawOfMessiahBibleReference.objects.none())

    def _query_references(self, query):
        query = query.select_related('law_of_messiah')
        for ref in query:
            ref.set_bible = lambda bible, ref=ref: setattr(ref, 'bible', bible)
            ref.set_bible(self.bible)
        return query
