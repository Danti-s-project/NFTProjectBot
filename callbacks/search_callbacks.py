from abstraction.callbacks.CallbackData import CallbackData


class ChoiceCollection(CallbackData, prefix="choice_collection"):
    collection_name: str


class ShowCollectionsPage(CallbackData, prefix="show_page"):
    direction: str

class Action(CallbackData, prefix="action"):
    action: str
