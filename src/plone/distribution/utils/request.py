from zope.i18n.interfaces import IUserPreferredLanguages
from zope.i18n.locales import LoadLocaleError
from zope.i18n.locales import locales


def extract_browser_language(request) -> str:
    """Extract browser language from request."""
    language = "en"
    pl = IUserPreferredLanguages(request)
    if pl is not None:
        languages = pl.getPreferredLanguages()
        for httplang in languages:
            parts = (httplang.split("-") + [None, None])[:3]
            if parts[0] == parts[1]:
                # Avoid creating a country code for simple languages codes
                parts = [parts[0], None, None]
            try:
                locale = locales.getLocale(*parts)
                language = locale.getLocaleID().replace("_", "-").lower()
                break
            except LoadLocaleError:
                # Just try the next combination
                pass
    return language
