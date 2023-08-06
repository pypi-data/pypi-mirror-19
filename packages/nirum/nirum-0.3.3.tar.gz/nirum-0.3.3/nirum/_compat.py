import datetime
import typing

__all__ = 'utc', 'is_union_type', 'get_union_types'


try:
    utc = datetime.timezone.utc
except AttributeError:
    ZERO = datetime.timedelta(0)
    HOUR = datetime.timedelta(hours=1)

    class UTC(datetime.tzinfo):
        """UTC"""

        def utcoffset(self, dt):
            return ZERO

        def tzname(self, dt):
            return "UTC"

        def dst(self, dt):
            return ZERO

    utc = UTC()


if hasattr(typing, 'UnionMeta'):
    def is_union_type(type_):
        return isinstance(type_, typing.UnionMeta)

    def get_union_types(type_):
        if is_union_type(type_):
            return type_.__union_params__
else:
    def is_union_type(type_):
        return isinstance(type_, typing._Union)

    def get_union_types(type_):
        if is_union_type(type_):
            return type_.__args__
