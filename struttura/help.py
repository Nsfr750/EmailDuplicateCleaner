from lang.lang import get_string

def get_help_content():
    """
    Returns the help content as a dictionary containing sections and their content.
    """
    return {
        "overview": {
            "title": get_string('help_overview_title'),
            "content": get_string('help_overview_content')
        },
        "features": {
            "title": get_string('help_features_title'),
            "content": get_string('help_features_content')
        },
        "getting_started": {
            "title": get_string('help_getting_started_title'),
            "content": get_string('help_getting_started_content')
        },
        "detection_criteria": {
            "title": get_string('help_detection_criteria_title'),
            "content": get_string('help_detection_criteria_content')
        },
        "cleaning_options": {
            "title": get_string('help_cleaning_options_title'),
            "content": get_string('help_cleaning_options_content')
        },
        "troubleshooting": {
            "title": get_string('help_troubleshooting_title'),
            "content": get_string('help_troubleshooting_content')
        },
        "faq": {
            "title": get_string('help_faq_title'),
            "content": get_string('help_faq_content')
        }
    }
