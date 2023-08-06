from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core import signing

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_jwt.settings import api_settings
from social_django.utils import load_strategy, load_backend
from social_core.actions import do_auth
from social_core.exceptions import MissingBackend
from rest_social_auth.views import SocialJWTUserAuthView

from .serializers import (
    LoginSerializer, RegisterSerializer, ActivateSerializer,
    ResendActivationMessageSerializer, SendResetPasswordMessageSerializer,
    ResetPasswordSerializer, ChangePasswordSerializer, ChangeEmailSerializer,
    ChangeEmailConfirmationSerializer
)
from . import utils as accounts_utils


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=False):
        # get username
        username_or_email = serializer.data['username_or_email']
        if '@' in username_or_email:
            try:
                username = get_user_model().objects \
                    .get(email=username_or_email).username
            except get_user_model().DoesNotExist:
                username = username_or_email
        else:
            username = username_or_email

        # try credentials
        user = authenticate(
            username=username,
            password=serializer.data['password']
        )
        if user is not None:
            # success
            payload = api_settings.JWT_PAYLOAD_HANDLER(user)
            token = api_settings.JWT_ENCODE_HANDLER(payload)
            response_payload = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER(
                token, user
            )
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'authInfo': response_payload,
                    'msg': _('You have been logged in.')
                }
            )
    return Response(
        status=status.HTTP_403_FORBIDDEN,
        data={'_error': _('Wrong username or password.')}
    )


@api_view(['POST'])
def social_login_begin(request, backend):
    strategy = load_strategy(request)
    try:
        redirect_uri = (
            settings.FRONTEND_ADDRESS +
            '/accounts/social-auth/' +
            backend +
            '/'
        )
        backend = load_backend(
            strategy=strategy,
            name=backend,
            redirect_uri=redirect_uri
        )
    except MissingBackend:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    auth = do_auth(backend)
    if auth:
        return Response({'url': auth.url})
    else:
        return Response(status=status.HTTP_500_SERVER_ERROR)


class SocialView(SocialJWTUserAuthView):
    def respond_error(self, error):
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'_error': str(error)}
        )

    def post(self, request, *args, **kwargs):
        res = super(SocialView, self).post(request, *args, **kwargs)
        if res.status_code != 200:
            return res
        token = res.data['token']
        user = get_user_model().objects.get(pk=res.data['id'])
        response_payload = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER(
            token, user
        )
        return Response(
            status=status.HTTP_200_OK,
            data={
                'authInfo': response_payload,
                'msg': _('You have been logged in.')
            }
        )


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = get_user_model().objects.create_user(
            username=serializer.data['username'],
            email=serializer.data['email'],
            password=serializer.data['password']
        )
        if settings.ACCOUNTS_ACTIVATION:
            user.is_active = False
            user.save()
            accounts_utils.send_activation_message(user, request)
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    'activation': True,
                    'msg': _('Your account has been created. Activation '
                             'message has been sent to provided email '
                             'address.')
                }
            )
        else:
            user = authenticate(
                username=serializer.data['username'],
                password=serializer.data['password']
            )
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    'msg': _('You account has been created. You can log in.')
                }
            )


@api_view(['POST'])
def activate(request):
    serializer = ActivateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        invalid_key_response = Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'_error': _('Activation key is invalid.')}
        )
        try:
            key_data = signing.loads(serializer.data['key'], max_age=60*15)
            if key_data.get('action') != 'ACTIVATE':
                return invalid_key_response
            try:
                user = get_user_model().objects.get(
                    pk=key_data['user'],
                    is_active=False,
                    last_login=None
                )
                if not user.is_active:
                    user.is_active = True
                    user.save()
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={'msg': _('Your account is now active. You can log '
                                   'in.')}
                )
            except get_user_model().DoesNotExist:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'msg': _('Activation key is not associated with any '
                                   'account that needs activation.')}
                )
        except signing.SignatureExpired:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'expired': True,
                    '_error': _('Activation key has expired.')
                }
            )
        except signing.BadSignature:
            return invalid_key_response


@api_view(['POST'])
def resend_activation_message(request):
    serializer = ResendActivationMessageSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            user = get_user_model().objects.get(
                email=serializer.data['email'],
                is_active=False,
                last_login=None
            )
            accounts_utils.send_activation_message(user, request)
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    'msg': _('Activation message has been sent to provided '
                             'email address.')
                }
            )
        except get_user_model().DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'_error': _('Provided email is not associated with any '
                                  'account that needs to be activated.')}
            )


@api_view(['POST'])
def send_reset_password_message(request):
    serializer = SendResetPasswordMessageSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            user = get_user_model().objects.get(email=serializer.data['email'])
            accounts_utils.send_reset_password_message(user, request)
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    'msg': _('Message with instructions how to change your '
                             'password has been sent to provided email '
                             'address.')
                }
            )
        except get_user_model().DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'_error': _('Provided email is not associated with any '
                                  'account.')}
            )


@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        invalid_key_response = Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'keyError': True,
                '_error': _('Change password key is invalid.')
            }
        )
        try:
            key_data = signing.loads(serializer.data['key'], max_age=60*15)
            if key_data.get('action') != 'RESET_PASSWORD':
                return invalid_key_response
            try:
                user = get_user_model().objects.get(pk=key_data['user'])
                user.set_password(serializer.data['password'])
                user.save()
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={'msg': _('Your password has been changed. You can '
                                   'log in.')}
                )
            except get_user_model().DoesNotExist:
                return invalid_key_response
        except signing.SignatureExpired:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'keyError': True,
                    '_error': _('Change password key has expired.')
                }
            )
        except signing.BadSignature:
            return invalid_key_response


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def change_password(request):
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid(raise_exception=True):
        request.user.set_password(serializer.data['new_password'])
        request.user.save()
        return Response(
            status=status.HTTP_200_OK,
            data={'msg': _('Your password has been changed.')}
        )


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def change_email(request):
    serializer = ChangeEmailSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        if settings.ACCOUNTS_ACTIVATION:
            accounts_utils.send_change_email_confirmation_message(
                new_email=serializer.data['new_email'],
                request=request
            )
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'msg': _('Confirmation messages has been sent to provided '
                             'email address.')
                }
            )
        else:
            request.user.email = serializer.data['new_email']
            request.user.save()
            return Response(
                status=status.HTTP_200_OK,
                data={'msg': _('Your email has been changed.')}
            )


@api_view(['POST'])
def change_email_confirmation(request):
    serializer = ChangeEmailConfirmationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        invalid_key_response = Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'keyError': True,
                '_error': _('Confirmation key is invalid.')
            }
        )
        try:
            key_data = signing.loads(serializer.data['key'], max_age=60*15)
            if key_data.get('action') != 'CHANGE_EMAIL':
                return invalid_key_response
            try:
                email_exists = get_user_model().objects \
                    .filter(email=key_data['new_email']).exists()
                if email_exists:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            '_error': _('Provided email address is already '
                                        'taken.')
                        }
                    )
                user = get_user_model().objects.get(pk=key_data['user'])
                user.email = key_data['new_email']
                user.save()
                return Response(
                    status=status.HTTP_200_OK,
                    data={'msg': _('Your email has been changed.')}
                )
            except get_user_model().DoesNotExist:
                return invalid_key_response
        except signing.SignatureExpired:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'keyError': True,
                    '_error': _('Confirmation key has expired.')
                }
            )
        except signing.BadSignature:
            return invalid_key_response
