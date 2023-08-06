import hmac as _hmac
import hashlib as _hashlib


def make_sig(form, secret):
    sig = ""
    for k in sorted(form.keys()):
        if form[k] is not None:
            sig += "{}{}".format(k, form[k])
    return _hmac.new(
        secret.encode('utf-8'), sig.encode('utf-8'), _hashlib.md5).hexdigest()
