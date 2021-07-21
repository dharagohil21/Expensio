"""
Author: Rushikesh Patel
"""
from typing import Union


def get_response_obj(
    message: str,
    data: Union[dict, list] = None,
    error = None,
):
    resp = {
        "success": True if not error else False,
        "message": message,
    }

    if error is not None:
        resp["error"] = error
    else:
        resp["data"] = data

    return resp