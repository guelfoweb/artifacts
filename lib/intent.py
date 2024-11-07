from . import match_regex

def info(folder):
    """Extracts intent information from files in the specified folder."""
    # https://developer.android.com/guide/components/intents-filters
    regex = {
        "intent": r"[A-Za-z]*\.intent\.[A-Za-z]*\.[A-Za-z0-9.]*",
        "intent_extra": r"[^\.](intent\.[A-Za-z]*\.[A-Za-z0-9.]*)",
    }
    exclude = []

    # Gather and sort results
    intent_matches = match_regex.inFolder(folder, regex["intent"], exclude)
    intent_extra_matches = match_regex.inFolder(folder, regex["intent_extra"], exclude)
    result = {"intent": sorted(intent_matches + intent_extra_matches)}

    return result


