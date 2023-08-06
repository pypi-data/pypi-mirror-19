from NucleusUtils.i18n.parser import get_raw_tags, Keyword, parsers
from . import defaults
from .locales import get_locale

default_locale = ''


def set_default_locale(name=default_locale):
    global default_locale
    default_locale = name


def raw_translate(key, locale=None, context=defaults.CONTEXT_NAME):
    if locale is None:
        locale = default_locale
    locale = get_locale(locale, context)
    if locale:
        return locale.get_translation(key)
    return key


def translate(key, locale=None, context=defaults.CONTEXT_NAME, parse=True, local_parsers=None, settings=None):
    if local_parsers is None:
        local_parsers = []
    if settings is None:
        settings = {}
    if locale is None:
        locale = default_locale
    text = raw_translate(key, locale, context)

    if not parse:
        return text

    for tag in get_raw_tags(text):
        keyword = Keyword.parse(tag)
        for parser in local_parsers + parsers:
            if parser.check(keyword, settings):
                text = parser.parse(text, keyword, settings)

    return text
