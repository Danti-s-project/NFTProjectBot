from abstraction.callbacks.CallbackData import CallbackData


class ProfileAction(CallbackData, prefix="profile_action"):
    """
    Нажатие кнопки в главном меню /profile
    """

    action: str