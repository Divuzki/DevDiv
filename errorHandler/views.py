from django.shortcuts import render

def view_404(request, *args, **kwargs):
    return render(request, "error.html")
