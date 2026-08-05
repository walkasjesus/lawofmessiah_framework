import vinaigrette


def register_translations(app_config):
    translatable_model_fields = {
        # Keep concise labels translatable via PO, but keep long commentary bodies out of PO.
        'LawOfMessiah': ['title', 'commandment'],
        'LawOfMessiahDrawing': ['title', 'description'],
        'Maimonides': ['commandment'],
    }

    # Register fields to translate
    for model, fields in translatable_model_fields.items():
        vinaigrette.register(app_config.get_model(model), fields)
