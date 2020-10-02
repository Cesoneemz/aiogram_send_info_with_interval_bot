from aiogram.dispatcher.filters.state import State, StatesGroup

class WaitForCsvWithInfo(StatesGroup):
    wait_for_csv_file = State()


class AddAdmin(StatesGroup):
    wait_for_admin_id = State()


class DeleteAdmin(StatesGroup):
    wait_for_admin_id_delete = State()

class EditSystemMessages(StatesGroup):
    wait_for_id = State()
    wait_for_new_message = State()


class SetIntervalToSendInfo(StatesGroup):
    wait_for_interval_in_seconds = State()
    wait_for_limit_query = State()


class DeleteMessageFromAnyway(StatesGroup):
    wait_for_id = State()
