import logging, json, sys

if (sys.version_info > (3, 0)):
    def unicode(value):
        return str(value)

    def long(value):
        return int(value)

from functools import wraps

from redis import StrictRedis

__version__ = '0.1.0'

class CachualCache(object):
    """Base class for all cache implementations. Provides the
    :meth:`~CachualCache.cached` decorator which can be applied to methods
    whose return value you want to cache. This class should not be used
    directly, and is meant to be subclassed.

    Subclasses should define a **get** method, which takes a single string
    argument, and returns the value in the cache for that key, or ``None`` in
    the case of a cache miss; and a **put** method, which takes three arguments
    for the cache key, the value to store, and a TLL (which may be none) and
    puts the value in the cache.
    """
    def __init__(self):
        self.logger = logging.getLogger("cachual")

    def cached(self, ttl=None, pack=None, unpack=None):
        """Functions decorated with this will have their return values cached.
        It should be used as follows::

            cache = RedisCache()

            @cache.cached()
            def method_to_be_cached(arg1, arg2, arg3='default'):
                ...

        A unique cache key will be generated for each function call, so that
        different values for the arguments will result in different cache keys.
        When you decorate a function with this, the cache will be checked
        first; if there is a cache hit, the value in the cache will be
        returned. Otherwise, the function is executed and the return value is
        put into the cache.

        Cache get/put failures are logged but ignored; if the cache goes down,
        the function will continue to execute as normal.

        :type ttl: integer
        :param ttl: The time-to-live in seconds. For caches that support TTLs,
                    the keys will expire after this time. If None (the
                    default), the cache default will be used (usually no
                    expiration).

        :type pack: function
        :param pack: If specified, this function will be called with the
                     decorated function's return value, and the result will be
                     stored in the cache. This can be used to alter the value
                     that actually gets stored in the cache in case you need to
                     process it first (e.g. dump a JSON string that is properly
                     escaped).

        :type unpack: function
        :param unpack: If specified, this function will be called with the
                       value from the cache in the event of a cache hit, and
                       the result will be returned to the caller. This can be
                       used to alter the value that gets returned from a cache
                       hit, in case you need to process it first (e.g. turn a
                       JSON string into a Python dictionary).
        """
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                key = self._get_key_from_func(f, args, kwargs)
                self.logger.debug("key: [%s]" % key)
                try:
                    value = self.get(key)
                    if value is not None:
                        self.logger.debug("got value from cache: %s" % value)
                        if unpack is not None:
                            return unpack(value)
                        return value
                except:
                    self.logger.warn("Error getting value", exc_info=1)

                self.logger.debug("no value from cache, calling function")
                value = f(*args, **kwargs)
                self.logger.debug("got value from function call: %s" % value)
                try:
                    packed = value if pack is None else pack(value)
                    self.put(key, packed, ttl)
                except:
                    self.logger.warn("Error putting value", exc_info=1)
                return value
            return decorated
        return decorator

    def _get_key_from_func(self, f, args, kwargs):
        """Internal function to build the cache key from the function and the
        args and kwargs it was called with."""
        if args:
            args_str = ', '.join([unicode(a) for a in args])
        else:
            args_str = None
        if kwargs:
            kwargs_str = ', '.join(\
                    ['%s=%s' % (unicode(k), unicode(kwargs[k]))\
                    for k in sorted(kwargs.keys())])
        else:
            kwargs_str = None

        prefix = f.__module__ + '.' + f.__name__
        suffix = ''
        if args_str is not None:
            suffix = '(' + args_str
            if kwargs_str is not None:
                suffix = suffix + ', ' + kwargs_str + ')'
            else:
                suffix = suffix + ')'
        else:
            if kwargs_str is not None:
                suffix = '(' + kwargs_str + ')'
            else:
                suffix = '()'

        return '%s%s' % (prefix, suffix)

class RedisCache(CachualCache):
    """A cache using Redis as the backing cache. All values will be stored as
    strings, meaning if you try to store non-string values in the cache, their
    unicode equivalent will be stored. If you want to alter this behavior e.g.
    to store Python dictionaries, use the pack/unpack arguments when you
    specify your @cached decorator.

    :type host: string
    :param host: The Redis host to use for the cache.

    :type port: integer
    :param port: The port to use for the Redis server.

    :type db: integer
    :param db: The Redis database to use on the server for the cache.

    :type kwargs: dict
    :param kwargs: Any additional args to pass to the :class:`CachualCache`
                   constructor.
    """
    def __init__(self, host='localhost', port=6379, db=0, **kwargs):
        super(RedisCache, self).__init__(**kwargs)
        self.client = StrictRedis(host=host, port=port, db=db)

    def get(self, key):
        """Get a value from the cache using the given key.
        
        :type key: string
        :param key: The cache key to get the value for.

        :returns: The value for the cache key, or None in the case of cache
                  miss.
        """
        return self.client.get(key)

    def put(self, key, value, ttl=None):
        """Put a value into the cache at the given key. If the value is not a
        string, its unicode value will be used. This behavior is defined by the
        underlying Redis library, and could be subject to change in future
        versions; thus it is safest to only store strings in Redis (although
        basic types should serialize into a string cleanly, you will need to
        unpack them when they are retrieved from the cache).

        :type key: string
        :param key: The cache key to use for the value.

        :param value: The value to store in the cache.

        :type ttl: integer
        :param ttl: The time-to-live for key in seconds, after which it will
                    expire.
        """
        self.client.set(key, value, ex=ttl)

def pack_json(value):
    """Pack the given JSON structure for storage in the cache by dumping it as
    a JSON string.

    :param value: The JSON structure (e.g. dict, list) to pack.

    :rtype: string
    :returns: The JSON structure as a JSON string.
    """
    return json.dumps(value)

def unpack_json(value):
    """Unpack the given string by loading it as JSON.

    :type value: string
    :param value: The string to unpack.

    :returns: The string as JSON.
    """
    return json.loads(value)

def unpack_int(value):
    """Unpack the given string into an integer.

    :type value: string
    :param value: The string to unpack.

    :rtype: integer
    :returns: The string as an integer.
    """
    return int(value)

def unpack_long(value):
    """Unpack the given string into a long.

    :type value: string
    :param value: The string to unpack.

    :rtype: long
    :returns: The string as a long.
    """
    return long(value)

def unpack_float(value):
    """Unpack the given string into a float.

    :type value: string
    :param value: The string to unpack.

    :rtype: float
    :returns: The string as a float.
    """
    return float(value)

def unpack_bool(value):
    """Unpack the given string into a boolean. 'True' will become True, and
    'False' will become False (as per the unicode values of booleans); anything
    else will result in a ValueError.

    :type value: string
    :param value: The string to unpack.

    :rtype: bool
    :returns: The string as a boolean.
    """
    if value == 'True':
         return True
    elif value == 'False':
         return False
    raise ValueError("Cannot convert %s to bool" % value)
