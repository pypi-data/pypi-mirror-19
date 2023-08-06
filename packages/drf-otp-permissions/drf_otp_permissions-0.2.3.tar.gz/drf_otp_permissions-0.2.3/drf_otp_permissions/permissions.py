"""
Provides a set of pluggable OTP permission policies.
"""
from __future__ import unicode_literals

from rest_framework.permissions import BasePermission

from .otp.validate import validate_otp


class IsValidOneTimePassword(BasePermission):
    """
    Allows access only to request with valid OTP in its header.
    """

    def has_permission(self, request, view):
        if hasattr(view, 'get_otp_key_location'):
            key_location = view.get_otp_key_location()
        else:
            key_location = getattr(view, 'otp_key_location', None)

        otp = request.META.get('HTTP_X_OTP', None)
        if not otp:
            otp = request.META.get('HTTP_X-OTP', None)
        return validate_otp(otp, request.data.dict(), key_location)