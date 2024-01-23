from storages import AlchemyBaseStorage
from models.models import UserHistory

class UserHistoryStorage(AlchemyBaseStorage):
    table = UserHistory
