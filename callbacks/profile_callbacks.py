from abstraction.callbacks.CallbackData import CallbackData


class ProfileAction(CallbackData, prefix="profile_action"):
    """
    Нажатие кнопки в главном меню /profile
    """

    action: str


class SettingsAction(CallbackData, prefix="profile_settings_action"):
    """
    Нажатие кнопки в настройках
    """

    action: str


class SelectLanguage(CallbackData, prefix="profile_select_language"):
    """
    Выбор языка в настройках языка
    """

    language: str