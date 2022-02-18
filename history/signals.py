from django.dispatch import Signal

object_viewed_signal = Signal(['instance', 'request'])
