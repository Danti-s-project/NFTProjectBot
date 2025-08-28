from abstraction.callbacks.CallbackData import CallbackData


class ChoiceCollection(CallbackData, prefix="choice_collection"):
    collection_name: str


class ShowCollectionsPage(CallbackData, prefix="show_collections_page"):
    direction: str


class ChoiceFilter(CallbackData, prefix="choice_filter"):
    filter_name: str
    filter_type: str


class ShowFilterPage(CallbackData, prefix="show_filter_page"):
    direction: str
    filter_type: str


class Action(CallbackData, prefix="action"):
    action: str
