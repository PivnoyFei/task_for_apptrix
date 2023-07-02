from django_filters import FilterSet
from django_filters.filters import NumberFilter

from users.models import CustomUser


class UserFilter(FilterSet):
    distance = NumberFilter(method='filter_is_distance', label='Дистанция')

    class Meta:
        model = CustomUser
        fields = ('gender', 'first_name', 'last_name', 'distance')

    def filter_is_distance(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return (
                queryset.exclude(id=self.request.user.id)
                .filter(distance__lte=value)
                .order_by('distance')
            )
        return queryset
