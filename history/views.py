from django.shortcuts import render, redirect
from .models import History
from django.views.generic import ListView, View
from django.views.generic.detail import SingleObjectMixin


class HistoryList(ListView):
    def get_queryset(self):
        user_history = History.objects.filter(user=self.request.user)
        return user_history


class HistoryDelete(SingleObjectMixin, View):
    model = History

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated and obj is not None:
            obj.delete()
        return redirect('history')
