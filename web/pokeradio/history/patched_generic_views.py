from django.views.generic import WeekArchiveView
from django.views.generic.dates import _date_from_string


class PatchedWeekArchiveView(WeekArchiveView):
    fk_date_field = None

    def get_dated_items(self):
        """
        Return (date_list, items, extra_context) for this request.
        """
        year = self.get_year()
        week = self.get_week()
        date_field = self.get_date_field()
        week_format = self.get_week_format()
        week_start = {
            '%W': '1',
            '%U': '0',
        }[week_format]
        date = _date_from_string(year, self.get_year_format(),
                            week_start, '%w',
                            week, week_format)
        since = self._make_date_lookup_arg(date)
        until = self._make_date_lookup_arg(self._get_next_week(date))

        # Patched To allow FK date_field
        if self.fk_date_field:
            date_field = self.fk_date_field

        lookup_kwargs = {
            '%s__gte' % date_field: since,
            '%s__lt' % date_field: until,
        }
        qs = self.get_dated_queryset(**lookup_kwargs)
        return (None, qs, {
            'week': date,
            'next_week': self.get_next_week(date),
            'previous_week': self.get_previous_week(date),
        })
