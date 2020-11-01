from . import translator

def translate(target, do_update=False):
    """Endpoint function that execute translation.

    Args:
        target (str): Name that you want to translate into Japanese.
        do_update (bool, optional): If True, English-Japansese dictionary will be updated. Defaults to False.

    Returns:
        [str]: Translated name.
    """
    return translator.translate(target, do_update)