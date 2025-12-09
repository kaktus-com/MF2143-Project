"""find_stuff.py

Provides a small, testable API that main.py expects:
- object_detected(obj_type, info=None)
- get_pressure_pad()
- get_basket()
- get_arrow()

The module stores the last detected object and its bounding box (xmin,xmax,ymin,ymax).
If `info` is not provided to `object_detected` the module will create a small
simulated/default bounding box for quick testing.

When a getter returns the stored info it resets the stored values (so the
information is consumed once, matching the earlier intent in the repo).
"""

from typing import Optional, Dict

# module-level state (intentionally empty/default-free)
# Other modules may set `find_stuff.object_information` directly after
# detecting an object. This module will no longer invent default boxes.
object_detected_last: Optional[str] = None
object_information: Optional[Dict[str, float]] = None


def object_detected(obj_type: str, info: Optional[Dict[str, float]] = None) -> None:
    """Register that an object of `obj_type` was detected.

    - `obj_type` should be a string like 'basket', 'pressure_pad', 'arrow'.
    - `info` is an optional dict with keys `xmin,xmax,ymin,ymax`.

    If `info` is not provided a default test box will be used. This makes
    the function safe to call from `main.py` where only a name may be passed.
    """
    global object_detected_last, object_information
    object_detected_last = obj_type
    # Do NOT create defaults here. If the caller provides `info`, store it;
    # otherwise clear `object_information` and expect the producer (e.g. the
    # vision/UART code) to set `find_stuff.object_information` directly.
    if info is None:
        object_information = None
    else:
        # keep a shallow copy to avoid accidental external mutation
        object_information = dict(info)


def _consume_object_information() -> Optional[Dict[str, float]]:
    """Return the currently stored object_information and clear the state.
    This mirrors the intended behaviour in the original file where information
    was reset after being read.
    """
    global object_detected_last, object_information
    if object_information is None:
        return None
    info = object_information
    # reset
    object_information = None
    object_detected_last = None
    return info


def get_pressure_pad() -> Optional[Dict[str, float]]:
    """Return pressure pad coordinates if the last detected object was a pad.
    The returned dict has keys `xmin,xmax,ymin,ymax` or None.
    """
    if object_detected_last == "pressure_pad":
        return _consume_object_information()
    return None


def get_basket() -> Optional[Dict[str, float]]:
    """Return basket coordinates if the last detected object was a basket."""
    if object_detected_last == "basket":
        return _consume_object_information()
    return None


def get_arrow() -> Optional[Dict[str, float]]:
    """Return arrow coordinates if the last detected object was an arrow."""
    if object_detected_last == "arrow":
        return _consume_object_information()
    return None


def set_object_information(obj_type: str, info: Dict[str, float]) -> None:
    """Explicitly set the detected object and its info (helper for tests)."""
    object_detected(obj_type, info)


# Small helper for external parsers that might call into this module when new
# data arrives (e.g. from UART). Keep this lightweight — parsing specifics
# belong to the code that reads the UART / vision system.
def parse_and_register_from_payload(payload: Dict) -> None:
    """Example hook: accepts a dict like {"type":"basket", "xmin":..}
    and registers the object. This keeps the module decoupled from the
    transport layer.
    """
    obj_type = payload.get("type")
    if obj_type is None:
        return
    info_keys = ("xmin", "xmax", "ymin", "ymax")
    if all(k in payload for k in info_keys):
        info = {k: float(payload[k]) for k in info_keys}
        object_detected(obj_type, info)
    else:
        # register detection without creating default info; allow external
        # code to populate `object_information` if available
        object_detected(obj_type)


__all__ = [
    "object_detected",
    "get_pressure_pad",
    "get_basket",
    "get_arrow",
    "set_object_information",
    "parse_and_register_from_payload",
    # expose globals so other modules can set/read them directly
    "object_detected_last",
    "object_information",
]