import os
import time
import datetime

from functools import wraps
from mongoengine import connect


def database(function):
    """Connect to local MongoDB instance"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        connect(db=os.environ['DB_NAME'])
        return function(*args, **kwargs)

    return wrapper


def delay(function):
    """Add delay to avoid rate limiting from MockAPI.io"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        time.sleep(1)
        return function(*args, **kwargs)

    return wrapper


def should_update(function):
    """Only trigger function if data need to be updated, and reformat data for remote API"""
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        # Check if should update
        updated_at = kwargs['data'].get('updatedAt') or kwargs['data'].get('createdAt')
        if not isinstance(updated_at, datetime.date):
            updated_at = datetime.datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S.%fZ')
            
        if self.last_updated_at and updated_at < self.last_updated_at:
            return False
            
        # Remove unecessary keys
        kwargs['data'].pop("_id", None)
        kwargs['data'].pop("ads", None)
        kwargs['data'].pop("adsets", None)
        kwargs['data'].pop("keywords", None)

        # Convert date fields to ISO format
        date_fields = ['createdAt', 'updatedAt']
        for date_field in date_fields:
            if kwargs['data'].get(date_field) and isinstance(kwargs['data'].get(date_field), datetime.date):
                kwargs['data'][date_field] = kwargs['data'][date_field].isoformat(timespec='milliseconds') + "Z"

        return function(self, *args, **kwargs)

    return wrapper