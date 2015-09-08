"""
Provides various authentication policies.
"""
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import HTTP_HEADER_ENCODING, exceptions
from players.models import Room


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


def authenticate_credentials(token):
    try:
        room = Room.objects.get(token=token)
    except Room.DoesNotExist:
        raise exceptions.AuthenticationFailed(_('Invalid token.'))

    return room


def authenticate(request):
    auth = get_authorization_header(request).split()

    if not auth or auth[0].lower() != b'token':
        return None

    if len(auth) == 1:
        msg = _('Invalid token header. No credentials provided.')
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = _('Invalid token header. Token string should not contain spaces.')
        raise exceptions.AuthenticationFailed(msg)

    try:
        token = auth[1].decode()
    except UnicodeError:
        msg = _('Invalid token header. Token string should not contain invalid characters.')
        raise exceptions.AuthenticationFailed(msg)

    return authenticate_credentials(token)
