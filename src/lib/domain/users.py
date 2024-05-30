import sys
sys.path.append('src')

from lib.database import MongoDB
from utils.constants import USER_DB


def create_user(**kwargs):
    """
    Create a new user and insert their information into the database.

    Args:
        **kwargs: User information.

    Returns:
        dict: Result of the insertion operation.
    """
    # with MongoDB() as db:
    #     kwargs['is_active'] = True
    #     result = db.insert_one(USER_DB, kwargs)

    # Convert ObjectId to string for serialization
    # result.update({"_id": str(kwargs.pop("_id")), **kwargs})

    return kwargs
