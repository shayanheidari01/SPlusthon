"""
This module holds several utilities regarding RSA and server fingerprints.
"""
import os
import struct
from hashlib import sha1
try:
    import rsa
    import rsa.core
except ImportError:
    rsa = None
    raise ImportError('Missing module "rsa", please install via pip.')

from ..tl import TLObject


# {fingerprint: (Crypto.PublicKey.RSA._RSAobj, old)} dictionary
_server_keys = {}


def get_byte_array(integer):
    """Return the variable length bytes corresponding to the given int"""
    # Operate in big endian (unlike most of SoroushPlus API) since:
    # > "...pq is a representation of a natural number
    #    (in binary *big endian* format)..."
    # > "...current value of dh_prime equals
    #    (in *big-endian* byte order)..."
    # Reference: https://core.telegram.org/mtproto/auth_key
    return int.to_bytes(
        integer,
        (integer.bit_length() + 8 - 1) // 8,  # 8 bits per byte,
        byteorder='big',
        signed=False
    )


def _compute_fingerprint(key):
    """
    Given a RSA key, computes its fingerprint like SoroushPlus does.

    :param key: the Crypto.RSA key.
    :return: its 8-bytes-long fingerprint.
    """
    n = TLObject.serialize_bytes(get_byte_array(key.n))
    e = TLObject.serialize_bytes(get_byte_array(key.e))
    # SoroushPlus uses the last 8 bytes as the fingerprint
    return struct.unpack('<q', sha1(n + e).digest()[-8:])[0]


def add_key(pub, *, old):
    """Adds a new public key to be used when encrypting new data is needed"""
    global _server_keys
    key = rsa.PublicKey.load_pkcs1(pub)
    _server_keys[_compute_fingerprint(key)] = (key, old)


def encrypt(fingerprint, data, *, use_old=False):
    """
    Encrypts the given data known the fingerprint to be used
    in the way SoroushPlus requires us to do so (sha1(data) + data + padding)

    :param fingerprint: the fingerprint of the RSA key.
    :param data: the data to be encrypted.
    :param use_old: whether old keys should be used.
    :return:
        the cipher text, or None if no key matching this fingerprint is found.
    """
    global _server_keys
    key, old = _server_keys.get(fingerprint, [None, None])
    if (not key) or (old and not use_old):
        return None

    # len(sha1.digest) is always 20, so we're left with 255 - 20 - x padding
    to_encrypt = sha1(data).digest() + data + os.urandom(235 - len(data))

    # rsa module rsa.encrypt adds 11 bits for padding which we don't want
    # rsa module uses rsa.transform.bytes2int(to_encrypt), easier way:
    payload = int.from_bytes(to_encrypt, 'big')
    encrypted = rsa.core.encrypt_int(payload, key.e, key.n)
    # rsa module uses transform.int2bytes(encrypted, keylength), easier:
    block = encrypted.to_bytes(256, 'big')
    return block


# Add default keys
# Soroush server RSA public keys (from Soroush JS client)
for pub in (
        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwACIRK5lXVLU/qPY1VuCssYQjNqh6dUr9UCmkHoOklt7X/Ki1Gqu
PeVx5VL3NLn64V1heDZqwKZ11NCSS+XBxXh5T2cXRf1Et5USaHtUcU6y0fDFWOBo
kyehfkJ4KHedI5Z6wkRdSxOVITeBLhIV9OYsa+MuOa7xiD9A8Ogh4Y7k+jA2/zPl
D41nej3OZEQnDIe762N6J54FzGuKVGtg+NSwkf/h1ULtSg5ifx9bj/vKDNhwdCrm
Q6IYeDsWwDYm6Rup+9+nUCA/khMpHpzNnEdUwcAa8HQeZCpJX7TZPZRew3T6VhS9
lv827e/5tL7bohxJrFlyf4BcRzP2I0Nu7QIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAv/rw/AHUhfRzC+DWbD2VNmtyBuaExqyi/RTVVUF8JcG1XffTjH5O
eBC2fJg6PoS+SWRNpKnMFVU+u5fU2SOYbENyJ1Czv5zdtE9YjkZ1yrhSbBPSKswi
IGLfIi/KEIj5faRPmyXjYjz/DqPk8lEVTn7Wx0XYB+bqJazXY09/DekOBM0RVEXJ
hRrcu1Uf4GdSwI8FvxvHhxKyaJRRPzqE0yNPriCvj93Zqfpsntf2bI632H8mETR5
H2AYr6WJr7PGJObP6DUv61MsJrqtv1SyBPTQrnqQdP2fWDontOA9cd3E8SPV3+zJ
wJFPQRBrpElz6ndNasr52KVVilHrm15zaQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAv/YC/prWQuLcHGgbZO/uqWURZ69oL2kNCc3ya+oFdvRHH/5k0qg3
tYPFSyVhikrSmetK7X/4QywC5+oxMtkXMFoE0RkRHmQpZg+1yLS0Yn1/jOVD95Xp
dI2jyNUjkqP+PpG5aPfZQaP4k7qVm8hNogXEFY4vKHhkIaELJyedWG0MQqnWck3V
8RDBoAa5P0gDd6ONbiOrNSObTCl3Y/v0msYS3QS0tPtrp/eufji4r4Q+JGxGfRFN
3FcYMkegQZYRb3pGEbORm+EVayO3mz3XGIhJRkI9VX/9pm1If0jAGo/6F6gsBQr9
vkx0YMl42Q9cqiyQJOg7mpmzfCH+k4vJUQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAv+mp2a2S4s1LHi9odLxVMWjkAcQiOI3bix5oHYptO6FqAH3t+Hx5
B8ULV6ZDvfmnuJG1z49Y7Nh9j7k03ZkRfX72aIwCHeBZAyfp0U85uQst0pA0wd/V
/hsmAyH7jk0Td2MW2c1oIA/5Uc5UN69p3Q18YKzoXQ1CKwiH10GeYzUoLfYYiank
ZdwVEuVxFLTjeqo0mg9EJW41byZn1/hJHrx0TGnUT2tOCdgblf2HQ4JmjTuhK8WH
aNLeExZgDGxOJlgbNVfCKlKJOuPQR/L6J8ptJ2BDfeSYccHmHC3SH9Myo+5qmvuV
o8imK4h4Rp7ruDQd8lzbxodiZZpI3hBkLQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAv/w2kmWGbK46B67b3b0gkRC9G4vOK5xWB0XBAripnvZjj8pq6OKL
cNyb+K5Cyw3icEQCXSGzAK84j4+dCrJo2Z2A1EhrxpRJ19/m0eTMnsw5fGZojGFF
MKFDyANW4dFb444Wdyp6MozYnchbm7RWePcp92CD2gQoM82Mp1wpZuf2ciI0ogOl
DYPIFmM3JSX57Aid/KutkOW+V3LWhE4JOW9PGsjrqTZ1VVMl0gdphQy0tvjU7HJG
XWivaGDN6WIe+Gww+VQe/1kUrz1kC9PEV0ShXEj7WH97CoATOpUJ74Ur2FM+tNn1
a3OwpcMAxyFtXQEE+XOrpbdRySB2BzURJQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAv/eAj+TK2zrFABaQ3o/qItzXOG5jrXB4sIQDR5cFbq7nLcajaasw
YOnIhGaoiG82jJh3bfqlbDrSO8JR9K0EXFYMcMTWO7OzqBCzCH43hv/VFLu5blBw
cx3VM9ke5r2jjLvkDn+SwVjsUuA6+eCEsxDzYOeCv2ZQOkol/11e2Eyhwjkxv72e
F4VERqHFjGN8biQKqNscm+4K4nNkgJbhH21SgWYA5Eh89M8tdkSxZrRkBCAR+tx4
zDv80so2VZm4JvZXhgh+tRagnkqBWaylUBoeo5w+Mnmx9sdLf1MQwFDzA1vX3LNw
Zze7PZ9p9bW72u9er4UuzO6/mVkv73KZlQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwAJUxxftspneFfcXRElZB7qMJcN8LOaXZyvf5hRRvWldeGsD3zZC
CSKndRCt7PiQtI27kBOjDF5XzMMGJ/aPLW0rMei/Q8aHHYYJuVGBAGPQX+5W0PPb
OKUPfujZanipb8EQKXWDzdG6zy3slilkSD+FEe4gwuQplKCJcxUlGbeM/naOgdHh
kOkCfC5xKejy4Q/N6AMjNZgLYjvoYOZz61eHRFf2TMR0aQr70yaAszddrIdX7AG/
LpKCVqx4i3i7JDN2Y57f/omEHX9Oo50ji3zjuWc+UD+nks+5g0MyFBVMMtmiLQbG
JceEyCIYXmw49rF60+NgjNfePpLYANs+KQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwAZB/1l/oV0UsYUnfDeaYLt2QomU6BX86P1Q83Y75CM1lcrsg5jV
YFwLyWrWExSdt9TM1kBzgqDJk4uOOjR04uRXhgjpI9+BT6vh357fT2DZLMHvDwfs
b5i88+IPgkbYzVhgbKl9GEsUgOOThE9duVnB4jChcg61jNIn8Gk1FKHbswcLG004
eQQYS075q5bubp1IVvlI/EyL12VAtiAvbWm95Ist17FDGvpCCrQHn5fTX1sWZa6n
dI4XkG2sctTiU2mKPkCz7VOXOlC2lIgkE+hwVtw9Uk+iMOFb6eMWQqXZfsZs9f8y
ktW4fhTZ3BA3ccbTzrpNEZeGVzR6UjMEBQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwAsNcJgXPEAyXwjkfUNAGMdk/PdoE0C2N+lg2DiOO1lGmFEKzPUc
mVwszSUBETQwAVg1gbNuo7jlspc/tPGWqzFMw0c5cNErtqBwZtTYs3fj9B4UwK9L
AS9Ow5s3aKJ7osxh0mdy+sBFGhcQy21v0WHNWec9an6FcbyCqms77g1DokLNvAtB
ym5JoaE0d5s+ScgA9kVvAij/hPOV922Nxr88ah8bQXDNDHa4LN7iBkAFnyie3nU6
LlZyphpCEGG26lZCu9sfupPdG+/LoBfOzTFykrlF4eAzhaj6EZvgwtu1/MrgNqAt
ndGxHSp6VCwPcKD0mPeXsJuKiuApfhJiAQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwCNBZIUIdL7eDklM3iecAAHMbjtjthDrfGL2o1oYbq21w/4tL5mi
Yhm20rhWsZD59UxSb4CosZDB8KpXlcmHSbMcjEwv5frchZjQhwEJO5A7U2eDcBdq
r9cnI5vUG/1I1/+b6w+5l/gPprhYhvAaKyZAsMlRygVcI2mnoKzlUs+OqLoFMaxI
0zvOs7QyWLkJ3LuF9arLrd5lYne5Cspt5lc+Iq3dGxbtgh10MBVvu7mSQaz3IO1P
XLsBY7wJ+sGOyctcL0oL0aK/Zz1AgqyX34XQMsuf/67+cj9W6zQn4gm2cS0Enhbg
DOFvmH8h8JgSTfNm2iLWnThLVoPiaLmjfQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwAgZjOzPCRtL1NY+M9vXDjJVF+5MCfkKMR71Wt0EIcI1PJMNdl9H
6/4Qos6rdD7JEwShziJM4yRpsLJqc70vAkb0flsR3Wyo0yrBgr/2xDmKJ2LuPRX8
4sU/Yv8BbfntpXfNLB60DRp0EhTIBhceg3A7Hu7/qAjdp6UXuL3aciXDJyvdGTnp
dtYNJPlu1unF5PivKGkqd57viZYvKREeybbXIVgF9TdTg8M/leF3aPLNokIKZztD
NQO5UFphCoYgEjFBGnTCYmg/J3Heh0rf+apW5NjfHm/y3puQcNe041I8tJOPhgq6
M3Kj9WtA8Vg8DB1JOaNmbcOmlOrYF9eKSQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwAiOBa1QUvz2UONwPBLuD7yUmbsamOecxmWCh04vNe+kN1k2B6cQ
RSmjIdaBux2ScYp0RvhbCw3XGVPXXkPb75zjsNUakHEgSi7HtT51wds62ph5HN11
6yI+itOAsoCWazu/dBlumBYtVnns05uDBB70+jkhS1juYncfvt9B2Jv6pAD92GVf
yLcx8c5Nmiuu8jBLql8139Dy96iCJdkF+eU2VDBIjLT/wLONAKTPtN5OwsZ3HUZ9
ndwyI3JDv06r+l+y1M3hpnxlvvU0bvPL0sTnm3rXcNSE+lmp0Z9GyqM+Udyejk52
vg2YquYhrhXba9PUhRXW+7w6sBd/rqDWyQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwAdLOUNYPhKgR2oO9YCEeIpH4ZKQcW0wgkMO8hfLXbAI3/Un0l0e
hMwNiv0Y7Xnu+QDKy57/a0uxCHzrzm8kIiM9zD7ek2ZlTUWDAw9je6jIp4NW54Ak
2WOj1MdUE2F/TSR5iZ1b0Ed7mDGbjbtRNs9IIK5t4oJPZHcztg8Ps8xLHFaOk9yE
WmUJNC+zsA/k2ZOGlsQDwBoEVncKkN8Clw+K/THS2+H2UvPoPMFpAlKhZmIXu1RX
pmeJNhk9Zs8g32OxAlF42EuWkYjf9O6pS9Dj7Lirxb7RWRu+jKjrrYmiGbzuqgMe
nOPBBO4xlob86vBWtNrjkDqooVCvQPAkwQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwAJKPTTSWIm7fPBmO9bGaLmwz/uAewFh4rSy1W0Y35EOYBMe/nki
LsMisaoia+4ySqr8geeuDT384JVddzL/tTZIpiAfvNxKbvJvErAF/4dB1Sv5MZ1q
H0Obo5JF5ifmfiVgaGKHChZrX7xs0Cb9RaOzyHKGnL1jvnTrDXCfSbjlfhf1wvwj
3F+8gn6ucuuh4UY7c9HfqzeNeMfaEuOVxN8WKIGLVfmnHTYzMyHwjSEqUUFakM87
66IJWDzBSb+7W3wZdvBiEHw3gFId+sSmDaqNdZuRLeMplabuOC88q8lX01TC4Jxr
DzrwBKLmXOK9WuiEXlJqc8ejiN9SBy+crQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwAO4JYhGwVXZpQBIb+efNiRVcA6YhgZVivN1ciicLRjQwCpQ+/k9
f6NCtY72kn8d17Cm1wo8uxV6WMgx0pvVj/FmjJDX7X4i7NkTI+hCwKDu0x89qYk7
/hXioXi4JoAYzb9xLRhyWDFXtAnR/VcdOxHgTlbP6RQxVQnQTNmXCSFq+EaRkPkA
Mrmas+aNuBkBWok6kp/Y0g04xJyILF30qqVLEokxw33R4KA9Af73QMaRecMJxOuF
rkexWXjoFvUq1hKJeMKLOKMSynM+a/1K+jyNsQcTTstFjCUhlXPwFRBsUP6h4wJI
hurY7/QbvbuQOaTMiM4nC1gr9g8FnD21zQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwAO9zS/84BlL8GrevNO2biWlsy1ijhMyuQOv8OYMqtKz7ekoz7J4
AD9hsGTbry/pRxf8nWR0SGqRQJ+C4Cz1MpafiyKJpP71DBKeDvi0f6+CGydw0p+B
DDPwuwIv+Blll9l/5fLNsELk8e6KBwCVI8TTHNFY94EXCGcBjk11/mvvlv6v1Rnz
FtNo0F1zUaVef+Bks4yL79/65HblPHfHnWmUMtGDWru8Nan++JrwuJzRVJTFaMPd
tIC52cTJ5OPtV7Ym0UHEfysYm91Ho+/Qxlm/hO6+qcF8FOggN9iysuiod4tOLv6R
98fvejH6H93oQ8qlWHVLXBfZ315UlDaVAQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwAcenoTdEuaHn+v9dKkwUMDp/9y4wv/f2tKoI6E/6o6jT7tXyiHV
esvC0iZJyFLwNwEOQk+/6QTdChldPwozyoGkwSgbRXrt/Ybdl6GvtkDXptz4OzVS
2hrZQMc6SdYTo2Ft1k8iLKgVhIafOjWV4w+Xz/mWBFX8+gLu8AXWDoznJ1hOmozv
3HjCDlx4WETxjG07JQnrVT/gPSiPvNd5zAIjdmkt+qVrwKTtHmrCqLPAn9oPVYT2
RKhrXPNPtKkR2fXNVM+VSXeKr5hH4nDDRSoaJF8FzIZ1+6S6KlvRzMSVTux41Z7i
CgiH64nhXI7+Kp/IzaAhgPpXkh8hiayckQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwBoDfGRxtbV4QTglS63QcvqtuCKaJLICtJDy+7yn1yj0+5qfCzJT
DUYefkMoghBHsaBRgekaRC0srPVnOHsZVLrYVXpkgpSpcWYMc4sSwrFOSyoEGdcu
eoSu/T40MtDWaAOfVOkGisGtMpR+7ot2K9GyjrscH/czCAdX9fHNTSLl2zrS82uv
RhJYHfNaOKGecAes3XLhtLdZTQ/0AIJSjT3UDAdmEpM+7SQCMcW7P2uEDa8w/6nF
wAi8mSAbdLwpnCpLqxBf9WvpN33ioWMPy2CSIaAKTb5DbL1DvcfNTv9GUL8ekQM+
tWTBd6SRRZXqss1XfQQnwRhTnAHab6RncQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwCDyIUUnsml5YkZq7kyEUHZo7/dd5kxn7uixApb94MFYcJNFupK5
5Wn8z1n6+1w+xZ/hvNgcSAIZ9Z4V/HRQsHccE0zzzLeoX7DeIRNiWh1cBaASlkOS
bmcuWP1Yy0NG3aYiPXerrMy2CBoYc5iFyOruOqCFGmXhNwTPfDA8TMlb4FGRdV93
u75MhiIDd1AZLS2k0SNGCss1FH9S9ks010lK5K3Xi71sDBHDuYy8ywpOXO0ZSFh0
AXyYILF4hRNWn32MA4J/gm3QmBGvjt1kVN8P9xnF1dqfVfeEYsPy4l9jWUHR3aEf
Y2j3RzdREMZUmfnZh/ziqM5uSn6stzOvuQIDAQAB
-----END RSA PUBLIC KEY-----''',

        '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAwB/rwrbaD86r79uhuOQz/vm5SZkBkHW3dsOejYZ/mhhVupNiTh6q
Sx/WfPhradZjn5QR5V2VxYNxPs/G1I6q3Mos49dnzxfz+8Rp4S+h8FyxGwJo3EOd
Bv+5BYHLAzrT1SNWt/wt+k5LbPF2AQpEwB8PzhgIe0a7MmPRv0/h6xv9rIBR403R
28T23X9hiy+Jruqwf6Iw4O4lWajbuNF4pVZGMH3aS1mJwoszTAIQgc0Uk3WinD9D
Fg8m+PFU126keVSWcuTpPRBCpDoU6nXdeYsISbe8WGN/CyfD1/gl1r14aN9fwwxp
eJzmIQvYNmlq5/zb2XxJpZMUAg3iS0nqTQIDAQAB
-----END RSA PUBLIC KEY-----''',
):
    add_key(pub, old=False)
