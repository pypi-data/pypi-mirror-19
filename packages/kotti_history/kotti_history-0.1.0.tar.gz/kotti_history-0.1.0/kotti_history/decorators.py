from pyramid import httpexceptions as httpexc


def login_required(wrapped):
    def wrapper(context, request):
        if request.user is not None:
            response = wrapped(context, request)
        else:
            raise httpexc.HTTPForbidden()
        return response
    return wrapper
