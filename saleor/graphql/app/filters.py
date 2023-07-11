import django_filters

from ...app import models
from ...app.types import AppExtensionTarget, AppType
from ..app.types import AppEventType
from ..core.filters import EnumFilter, ListObjectTypeFilter, ObjectTypeFilter
from ..core.types import DateTimeRangeInput
from ..utils.filters import filter_range_field
from .enums import (
    AppEventTypeEnum,
    AppExtensionMountEnum,
    AppExtensionTargetEnum,
    AppTypeEnum,
)


def filter_app_search(qs, _, value):
    if value:
        qs = qs.filter(name__ilike=value)
    return qs


def filter_app_event_type(qs, _, value):
    if value in [type for type, _ in AppEventType.CHOICES]:
        qs = qs.filter(type=value)
    return qs


def filter_created_at(qs, _, value):
    return filter_range_field(qs, "date", value)


def filter_app_type(qs, _, value):
    if value in [AppType.LOCAL, AppType.THIRDPARTY]:
        qs = qs.filter(type=value)
    return qs


def filter_app_extension_target(qs, _, value):
    if value in [target for target, _ in AppExtensionTarget.CHOICES]:
        qs = qs.filter(target=value)
    return qs


def filter_app_extension_mount(qs, _, value):
    if value:
        qs = qs.filter(mount__in=value)
    return qs


class AppFilter(django_filters.FilterSet):
    type = EnumFilter(input_class=AppTypeEnum, method=filter_app_type)
    search = django_filters.CharFilter(method=filter_app_search)
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = models.App
        fields = ["search", "is_active"]


class AppExtensionFilter(django_filters.FilterSet):
    mount = ListObjectTypeFilter(
        input_class=AppExtensionMountEnum, method=filter_app_extension_mount
    )
    target = EnumFilter(
        input_class=AppExtensionTargetEnum, method=filter_app_extension_target
    )

    class Meta:
        model = models.AppExtension
        fields = ["mount", "target"]


class AppEventFilter(django_filters.FilterSet):
    type = EnumFilter(input_class=AppEventTypeEnum, method=filter_app_event_type)
    created_at = ObjectTypeFilter(
        input_class=DateTimeRangeInput, method=filter_created_at
    )

    class Meta:
        model = models.AppEvent
        fields = ["type", "created_at"]
