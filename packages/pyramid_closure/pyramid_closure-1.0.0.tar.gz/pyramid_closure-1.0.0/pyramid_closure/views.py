from itertools import chain

from pyramid.settings import aslist
from six import string_types

from .closure import depswriter


def flatten(l):
    "Flatten one level of nesting"
    return chain.from_iterable(l)


def pairwise(iterable):
    a = flatten(iterable)
    return zip(a, a)


def depsjs(request):
    path_to_source = {}

    settings = request.registry.settings
    pyramid_closure = settings.get("pyramid_closure")

    roots = pyramid_closure.get("roots") if pyramid_closure else \
        settings.get("pyramid_closure.roots")

    if roots is None:
        roots = []
    elif isinstance(roots, string_types):
        roots = aslist(roots)

    for root in roots:
        path_to_source.update(depswriter._GetRelativePathToSourceDict(root))

    roots_with_prefix = pyramid_closure.get("roots_with_prefix") if \
        pyramid_closure else \
        settings.get("pyramid_closure.roots_with_prefix")

    if roots_with_prefix is None:
        roots_with_prefix = []
    elif isinstance(roots_with_prefix, string_types):
        roots_with_prefix = [aslist(roots_with_prefix)]

    for prefix, root in pairwise(roots_with_prefix):
        path_to_source.update(
            depswriter._GetRelativePathToSourceDict(
                root, prefix=request.static_url(prefix)))

    request.response.content_type = 'text/javascript'

    return depswriter.MakeDepsFile(path_to_source)
