from django.shortcuts import render


def page_not_found(request, exception):
    template_name = "errors/404error.html"
    return render(request, template_name)


def error(request):
    template_name = "errors/500error.html"
    return render(request, template_name)


def permission_denied(request, exception):
    template_name = "errors/403error.html"
    return render(request, template_name)


def bad_request(request, exception):
    template_name = "errors/400error.html"
    return render(request, template_name)
