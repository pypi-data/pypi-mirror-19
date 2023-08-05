from django.utils.translation import ugettext_lazy as _

from howl.operators import BaseOperator


class MyOperator(BaseOperator):
    display_name = _('My +2')

    def compare(self, compare_value):
        return compare_value > (self.observer.value + 2.0)
