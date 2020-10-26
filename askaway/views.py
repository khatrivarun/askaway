from django.shortcuts import redirect


def landing(request):
    return redirect('/questions/all')
