import vinaigrette


def register_translations(app_config):
    translatable_model_fields = {
        'LawOfMessiah': ['title', 'commandment', 'commentary_rudolph', 'commentary_juster', 'classical_commentators'],
        'LawOfMessiahDrawing': ['title', 'description'],
        'Maimonides': ['commandment'],
    }

    # Register fields to translate
    for model, fields in translatable_model_fields.items():
        vinaigrette.register(app_config.get_model(model), fields)
