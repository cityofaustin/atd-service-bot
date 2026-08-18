import json
import logging
from pprint import pformat


def describe_shape(obj, *, depth=2):
    """Return a JSON-serializable summary of an object's structure."""
    if isinstance(obj, list):
        if not obj:
            return {"type": "list", "len": 0}
        item_shape = (
            describe_shape(obj[0], depth=depth - 1)
            if depth > 0
            else type(obj[0]).__name__
        )
        return {"type": "list", "len": len(obj), "item": item_shape}
    if isinstance(obj, dict):
        if depth <= 0:
            return {"type": "dict", "len": len(obj), "keys": sorted(map(str, obj.keys()))}
        values = obj.values()
        homogeneous_scalars = obj and all(
            v is None or isinstance(v, (str, int, float, bool)) for v in values
        )
        if homogeneous_scalars and len(obj) > 20:
            sample = list(obj.items())[:5]
            return {
                "type": "dict",
                "len": len(obj),
                "sample": {str(k): v for k, v in sample},
            }
        return {
            "type": "dict",
            "len": len(obj),
            "fields": {
                str(k): describe_shape(v, depth=depth - 1) for k, v in obj.items()
            },
        }
    if obj is None:
        return None
    return type(obj).__name__


def log_data(label, data, verbosity):
    """Log payload shape at -v; also dump the payload at -vv."""
    if verbosity < 1:
        return
    logging.info(
        "%s shape: %s", label, json.dumps(describe_shape(data), indent=2, default=str)
    )
    if verbosity >= 2:
        logging.info("%s data:\n%s", label, pformat(data))
