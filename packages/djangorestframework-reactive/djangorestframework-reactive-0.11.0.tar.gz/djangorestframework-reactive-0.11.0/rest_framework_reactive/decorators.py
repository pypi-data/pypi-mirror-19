from rest_framework import response

from . import client, request as observer_request

observer_client = client.QueryObserverClient()


def observable(method):
    """
    A decorator, which makes the specified ViewSet method observable. If the
    decorated method returns a response containing a list of items, it must use
    the provided `LimitOffsetPagination` for any pagination. In case a non-list
    response is returned, the resulting item will be wrapped into a list.

    When multiple decorators are used, `observable` must be the first one
    to be applied as it needs access to the method name.
    """

    def wrapper(self, request, *args, **kwargs):
        if 'observe' in request.query_params:
            # TODO: Validate the session identifier.
            session_id = request.query_params['observe']
            data = observer_client.create_observer(
                observer_request.Request(self.__class__, method.__name__, request, args, kwargs),
                session_id
            )
            return response.Response(data)
        else:
            # Non-reactive API.
            return method(self, request, *args, **kwargs)

    wrapper.is_observable = True

    # Copy over any special observable attributes.
    for attribute in dir(method):
        if attribute.startswith('observable_'):
            setattr(wrapper, attribute, getattr(method, attribute))

    return wrapper


def primary_key(name):
    """
    A decorator which configures the primary key that should be used for
    tracking objects in an observable method.

    :param name: Name of the primary key field
    """

    def decorator(method):
        method.observable_primary_key = name
        return method

    return decorator
