from deep_translator import GoogleTranslator


def translate(text, source='auto', target='en'):

    return GoogleTranslator(source=source, target=target).translate(text)