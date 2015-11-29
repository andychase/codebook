import base64
import hmac
import hashlib
import urllib.parse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.conf import settings


@login_required
def sso(request):
    payload = request.GET.get('sso')
    signature = request.GET.get('sig')

    if None in [payload, signature]:
        return HttpResponseBadRequest('No SSO payload or signature. Please contact support if this problem persists.')

    # Validate the payload

    payload = bytes(urllib.parse.unquote(payload), "utf-8")
    decoded = base64.decodebytes(payload)

    key = bytes(str(settings.DISCOURSE_SSO_SECRET), "utf-8")
    h = hmac.new(key, payload, digestmod=hashlib.sha256)
    this_signature = h.hexdigest()

    if this_signature != signature:
        return HttpResponseBadRequest('Invalid payload. Please contact support if this problem persists.')

    # Build the return payload

    qs = urllib.parse.parse_qs(decoded)
    params = {
        'nonce': qs[b'nonce'][0],
        'email': request.user.email,
        'external_id': request.user.id,
        'username': request.user.username,
    }

    return_payload = base64.encodebytes(bytes(urllib.parse.urlencode(params), "utf-8"))
    h = hmac.new(key, return_payload, digestmod=hashlib.sha256)
    query_string = urllib.parse.urlencode({'sso': return_payload, 'sig': h.hexdigest()})

    # Redirect back to Discourse

    url = qs[b'return_sso_url'][0].decode('utf-8')
    return HttpResponseRedirect('%s?%s' % (url, query_string))
