import enum


class Locale(str, enum.Enum):
    EN = "en"
    RU = "ru"
    ZH = "zh"  # Китайский


class SystemMessages(str, enum.Enum):
    START_MESSAGE = "start_message"
    SELECT_COLLECTION_MESSAGE = "select_collection_message"
    SET_FILTERS_MESSAGE = "set_filters_message"
    SELECT_MODEL_MESSAGE = "select_model_message"
    SELECT_SYMBOL_MESSAGE = "select_symbol_message"
    SELECT_BACKDROP_MESSAGE = "select_backdrop_message"

    SEARCH_RESULT_HEADER_TEXT = "search_result_header_text"
    SEARCH_RESULT_MODEL_TEXT = "search_result_model_text"
    SEARCH_RESULT_SYMBOL_TEXT = "search_result_symbol_text"
    SEARCH_RESULT_BACKDROP_TEXT = "search_result_backdrop_text"
    SEARCH_RESULT_OWNER_TEXT = "search_result_owner_text"

    BACK_BUTTON_TEXT = "back_button_text"
    FORWARD_BUTTON_TEXT = "forward_button_text"
    SELECT_BACKDROP_BUTTON_TEXT = "select_backdrop_button_text"
    SELECT_SYMBOL_BUTTON_TEXT = "select_symbol_button_text"
    SELECT_MODEL_BUTTON_TEXT = "select_model_button_text"
    SELECT_BACKDROP_EXISTS_BUTTON_TEXT = "select_backdrop_exists_button_text"
    SELECT_SYMBOL_EXISTS_BUTTON_TEXT = "select_symbol_button_text"
    SELECT_MODEL_EXISTS_BUTTON_TEXT = "select_model_button_text"
    SEARCH_BUTTON_TEXT = "search_button_text"
