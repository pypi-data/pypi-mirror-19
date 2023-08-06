from __future__ import unicode_literals

import json
from datetime import datetime, timedelta
import time
import logging

from .encryptions import decrypt_message_with_file
from .encryptions import encrypt_message_with_file

logger = logging.getLogger(__name__)


def _str_dict(data):
    output_dict = {}
    for key, value in list(data.items()):
        output_dict[str(key)] = str(value)
    return output_dict


def create_otp(data, key_location):
    """
    Given data and key location, return OTP header for HTTP request
    :param data: dict. Data passed with the HTTP request
    :param key_location: str. Path to encryption key
    :return: str. Encryption of `data` and current time
    """
    datetime_object = datetime.utcnow()
    delta = timedelta(seconds=60)
    due = datetime_object + delta
    unix_time = time.mktime(due.timetuple())

    str_data = _str_dict(data)

    message_dict = {
        "data": str_data,
        "due": unix_time
    }

    message_json_str = json.dumps(message_dict)

    return encrypt_message_with_file(message_json_str, key_location)


def validate_otp(otp, data, key_location):
    """
    Given otp, data, and key location, validate if OTP is correct
    :param otp: str. Encryption of `data` and created time
    :param data: dict. Data passed with HTTP request
    :return: bool. True, if OTP is valid. Else, returns False.
    """
    if not otp:
        logger.info(type(otp))
        logger.info("empty otp was provided: %s" % str(otp))
        return False

    try:
        decrypted_string = decrypt_message_with_file(otp, key_location)
    except Exception as e:
        logger.error(str(e))
        logger.info("failed to decrypt %s" % otp)
        return False

    try:
        decrypted_message_dict = json.loads(decrypted_string)
    except Exception as e:
        logger.error(str(e))
        logger.info("failed to parse json from %s" % decrypted_string)
        return False

    decrypted_data = decrypted_message_dict.get("data", {})

    encode_data = {}
    for k, v in decrypted_data.items():
        if type(k) is str:
            k = k.decode('utf8')
        if type(v) is str:
            v = v.decode('utf8')
        encode_data[k] = v

    if encode_data != data:
        logger.info("encode_data does not equal to data")
        logger.info("encode_data = %s" % str(encode_data))
        logger.info("data = %s" % str(data))
        return False

    decrypted_due = decrypted_message_dict.get('due')
    if not decrypted_due:
        logger.warn('due omitted')
        return False

    try:
        datetime_object = datetime.fromtimestamp(decrypted_due)
    except Exception as e:
        logger.error(str(e))
        logger.info("failed to parse datetime from %s" % str(decrypted_due))
        return False

    if datetime.utcnow() < datetime_object:
        return True
    return False