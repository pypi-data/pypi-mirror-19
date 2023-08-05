"""
Some common functions
"""
from __future__ import division
import os
import re
import inspect
import time
import datetime
import string
import random
import socket
import subprocess
import functools
import multiprocessing
import threading
from passlib.hash import bcrypt as crypt_engine
from six.moves.urllib.parse import urlparse, urlencode, unquote_plus as urllib_unquote_plus
import humanize
import pkg_resources
import urllib
import hashlib
import json
import uuid
from . import exceptions
from slugify import slugify
from werkzeug.utils import import_string
from distutils.dir_util import (copy_tree as copy_dir,
                                remove_tree as remove_dir,
                                mkpath as make_dirs)
from distutils.file_util import copy_file, move_file
from inflection import (dasherize, underscore, camelize, pluralize,
                        singularize, titleize)
import itsdangerous

# deprecated, no longer global. Needs to import utils
__all__ = [
    "is_email_valid",
    "is_password_valid",
    "is_url_valid",
    "urlencode",
    "urldecode",
    "urlparse",
    "md5",
    "slugify",
    "underscore",
    "dasherize",
    "camelize",
    "pluralize",
    "singularize",
    "titleize",
    "chunk_list",
    "guid",
    "in_any_list",
    "sign_jwt",
    "unsign_jwt"
]

def is_email_valid(email):
    """
    Check if email is valid
    """
    pattern = re.compile(r'[\w\.-]+@[\w\.-]+[.]\w+')
    return bool(pattern.match(email))


def is_password_valid(password):
    """
    Check if a password is valid
    """
    pattern = re.compile(r"^.{4,75}$")
    return bool(pattern.match(password))


def is_url_valid(url):
    """
    Check if url is valid
    """
    pattern = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            #r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))


def urldecode(s):
    return urllib_unquote_plus(s)


def md5(value):
    """
    Create MD5
    :param value:
    :return:
    """
    m = hashlib.md5()
    m.update(value)
    return str(m.hexdigest())


def guid():
    """
    Creates and returns a UUID 4 hex value
    :return: string
    """
    return uuid.uuid4().hex


def chunk_list(items, size):
    """
    Return a list of chunks
    :param items: List
    :param size: int The number of items per chunk
    :return: List
    """
    size = max(1, size)
    return [items[i:i + size] for i in range(0, len(items), size)]


def in_any_list(items1, items2):
    """
    Check if any items are in list 3
    :param items1: list
    :param items2: list
    :return:
    """
    return any(i in items2 for i in items1)


def encrypt_string(string):
    """
    Encrypt a string
    """
    return crypt_engine.encrypt(string)


def verify_encrypted_string(string, encrypted_string):
    """
    Verify an encrypted string
    """
    return crypt_engine.verify(string, encrypted_string)


def generate_random_string(length=8):
    """
    Generate a random string
    """
    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set * (length - 1), length))


def generate_random_hash(size=32):
    """
    Return a random hash key
    :param size: The max size of the hash
    :return: string
    """
    return os.urandom(size//2).encode('hex')


def how_old(dob):
    """
    Calculate the age
    :param dob: datetime object
    :return: int
    """
    today = datetime.date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def is_port_open(port, host="127.0.0.1"):
    """
    Check if a port is open
    :param port:
    :param host:
    :return bool:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, int(port)))
        s.shutdown(2)
        return True
    except Exception as e:
        return False

def create_uri(host, user=None, password=None, port=None, path=None, scheme="http"):
    port = ":%s" % port if port else ""
    path = "/%s" % path if path else ""
    user_info = ""
    if user or password:
        user_info = "%s:%s@" % (user or "", password or "")
    return "{scheme}://{user_info}{host}{port}{path}".format(
        scheme=scheme, host=host, user_info=user_info,port=port, path=path)


class dictdot(dict):
    """
    A dict extension that allows dot notation to access the data.
    ie: dict.get('key.key2.0.keyx')
    my_dict = {...}
    d = dictdot(my_dict)
    d.get("key1")
    d.get("key1.key2")
    d.get("key3.key4.0.keyX")

    Still have the ability to access it as a normal dict
    d[key1][key2]
    """
    def get(self, key, default=None):
        """
        Access data via
        :param key:
        :param default: the default value
        :return:
        """
        try:
            val = self
            if "." not in key:
                return self[key]
            for k in key.split('.'):
                if k.isdigit():
                    k = int(k)
                val = val[k]
            return val
        except (TypeError, KeyError, IndexError) as e:
            return default


def sign_jwt(data, secret_key, expires_in, salt=None, **kw):
    """
    To create a signed JWT
    :param data:
    :param secret_key:
    :param expires_in:
    :param salt:
    :param kw:
    :return: string
    """
    try:
        s = itsdangerous.TimedJSONWebSignatureSerializer(secret_key=secret_key,
                                                         expires_in=expires_in,
                                                         salt=salt,
                                                          **kw)
        return s.dumps(data)

    except itsdangerous.BadData as e:
        raise exceptions.MamboExtensionError(e)

def unsign_jwt(token, secret_key, salt=None, **kw):
    """
    To unsign a JWT token
    :param token:
    :param kw:
    :return: mixed data
    """
    try:
        s = itsdangerous.TimedJSONWebSignatureSerializer(secret_key, salt=salt, **kw)
        return s.loads(token)
    except itsdangerous.BadData as e:
        raise exceptions.MamboExtensionError(e)


class TimestampSigner2(itsdangerous.TimestampSigner):
    expires_in = 0

    def get_timestamp(self):
        now = datetime.datetime.utcnow()
        expires_in = now + datetime.timedelta(seconds=self.expires_in)
        return int(expires_in.strftime("%s"))

    @staticmethod
    def timestamp_to_datetime(ts):
        return datetime.datetime.fromtimestamp(ts)


class URLSafeTimedSerializer2(itsdangerous.URLSafeTimedSerializer):
    default_signer = TimestampSigner2

    def __init__(self, secret_key, expires_in=3600, salt=None, **kwargs):
        self.default_signer.expires_in = expires_in
        super(self.__class__, self).__init__(secret_key, salt=salt, **kwargs)


def sign_url_safe(data, secret_key, expires_in=None, salt=None, **kw):
    """
    To sign url safe data.
    If expires_in is provided it will Time the signature
    :param data:
    :param secret_key:
    :param expires_in:
    :param salt:
    :param kw:
    :return:
    """
    try:
        if expires_in:
            s = URLSafeTimedSerializer2(secret_key=secret_key,
                                        expires_in=expires_in,
                                        salt=salt,
                                        **kw)
        else:
            s = itsdangerous.URLSafeSerializer(secret_key=secret_key,
                                               salt=salt,
                                               **kw)
        return s.dumps(data)
    except itsdangerous.BadData as e:
        raise exceptions.MamboExtensionError(e)


def unsign_url_safe(token, secret_key, salt=None, **kw):
    """
    To sign url safe data.
    If expires_in is provided it will Time the signature
    :param token:
    :param secret_key:
    :param salt:
    :param kw:
    :return:
    """
    try:
        if len(token.split(".")) == 3:
            s = URLSafeTimedSerializer2(secret_key=secret_key, salt=salt, **kw)
            value, timestamp = s.loads(token, max_age=None, return_timestamp=True)
            now = datetime.datetime.utcnow()
            if timestamp > now:
                return value
            else:
                raise itsdangerous.SignatureExpired(
                    'Signature age %s < %s ' % (timestamp, now),
                    payload=value,
                    date_signed=timestamp)
        else:
            s = itsdangerous.URLSafeSerializer(secret_key=secret_key, salt=salt, **kw)
            return s.loads(token)
    except itsdangerous.BadData as e:
        raise exceptions.MamboExtensionError(e)

# ----
# COULD BE DEPRECATED

def get_pkg_resources_filename(pkg, filename=""):
    """
    Returns a string filepath from a package name/path
    It helps get the full path from a package directory
    :param pkg: str - The dotted path of package dir: portofolio.component, or mambo.component.views
    :param filename: str - The file or dir name to use use
    returns str
    """
    return pkg_resources.resource_filename(pkg, filename)


def get_domain_name(url):
    """
    Get the domain name
    :param url:
    :return:
    """
    if not url.startswith("http"):
        url = "http://" + url
    if not is_url_valid(url):
        raise ValueError("Invalid URL '%s'" % url)
    parse = urlparse(url)
    return parse.netloc


def seconds_to_time(sec):
    """
    Convert seconds into time H:M:S
    """
    return "%02d:%02d" % divmod(sec, 60)


def time_to_seconds(t):
    """
    Convert time H:M:S to seconds
    """
    l = list(map(int, t.split(':')))
    return sum(n * sec for n, sec in zip(l[::-1], (1, 60, 3600)))


def convert_bytes(bytes):
    """
    Convert bytes into human readable
    """
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size


def time_ago(dt):
    """
    Return the current time ago
    """
    now = datetime.datetime.now()
    return humanize.naturaltime(now - dt)

# ------------------------------------------------------------------------------
# Background multi processing and threading
# Use the decorators below for background processing

def bg_process(func):
    """
    A multiprocess decorator
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        p = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        p.start()
    return wrapper

def bg_thread(func):
    """
    A threading decorator
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        p = threading.Thread(target=func, args=args, kwargs=kwargs)
        p.start()
    return wrapper


# ------------------------------------------------------------------------------




# ---


class InspectDecoratorCompatibilityError(Exception):
    pass


class _InspectMethodsDecorators(object):
    """
    This class attempt to retrieve all the decorators in a method
    """
    def __init__(self, method):
        self.method = method
        self.decos = []

    def parse(self):
        """
        Return the list of string of all the decorators found
        """
        self._parse(self.method)
        return list(set([deco for deco in self.decos if deco]))

    @classmethod
    def extract_deco(cls, line):
        line = line.strip()
        if line.startswith("@"):
            if "(" in line:
                line = line.split('(')[0].strip()
            return line.strip("@")

    def _parse(self, method):
        argspec = inspect.getargspec(method)
        args = argspec[0]
        if args and args[0] == 'self':
            return argspec
        if hasattr(method, '__func__'):
            method = method.__func__
        if not hasattr(method, '__closure__') or method.__closure__ is None:
            raise InspectDecoratorCompatibilityError

        closure = method.__closure__
        for cell in closure:
            inner_method = cell.cell_contents
            if inner_method is method:
                continue
            if not inspect.isfunction(inner_method) \
                and not inspect.ismethod(inner_method):
                continue
            src = inspect.getsourcelines(inner_method)[0]
            self.decos += [self.extract_deco(line) for line in src]
            self._parse(inner_method)


def get_decorators_list(method):
    """
    Shortcut to InspectMethodsDecorators
    :param method: object
    :return: List
    """
    kls = _InspectMethodsDecorators(method)
    return kls.parse()




