Configi
=======

Configi is a straightforward wrapper for configuration data. It provides a consistent interface to a number of back-ends, currently via arbitrary HTTP JSON loading, Redis K/V store, and S3 JSON file loading.

Using Configi
-------------

The code itself is documented, but here's a couple of recipes:

S3 Config Source
~~~~~~~~~~~~~~~~
.. code-block:: python

    from configi import DynamicConfig, S3ConfigSource
    import boto     # Boto not included, but if you want to use S3ConfigSource
                    # you probably have it already. I hope.

    s3 = boto.connect_s3()
    bucket = s3.get_bucket("my-config-repository")
    config_file_key = bucket.get_key("my-config-file-key")

    source = S3ConfigSource(config_file_key)
    config = DynamicConfig(
                    source,
                    expiry=(60*4),  # Every four hours reload
                    quiet_mode=True,  # Errors will `print` instead of throwing Exceptions.
                    namespace_dicts=True,  # Turn dictionaries into dot-accessible namespaces.
                    defaults={'some_key': 'a_value'}  # Defaults dict is used to return values, if a key is unset remotely.
                )

    print config.foo
        > None

    config.foo = 'bar'
    print config.foo
        > bar

    print config.some_key
        > a_value

    config.some_key = 'banana'
    print config.some_key
        > banana

Redis Config Source
~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    from configi import DynamicConfig, RedisConfigSource
    import redis    # Redis not included, but if you want to use
                    # RedisConfigSource, then you'll need it.

    r = redis.StrictRedis()  # Get a Redis connection. Yours will have more parameters.
    source = RedisConfigSource(r, prefix='MY_AWESOME_CONFIGI_CONFIG_SETUP:')    # Default prefix is 'CONFIGI:'
    config = DynamicConfig(
                    source,
                    expiry=(60*4),  # Every four hours reload
                    quiet_mode=True,  # Errors will `print` instead of throwing Exceptions.
                    namespace_dicts=True,  # Turn dictionaries into dot-accessible namespaces.
                    defaults={'some_key': 'a_value'}  # Defaults dict is used to return values, if a key is unset remotely.
                )

    print config.foo
        > None

    config.foo = 'bar'
    print config.foo
        > bar

    print config.some_key   # Even though defaults were passed, any remotely-set value overrides.
        > orangutan


JSON File Config Source
~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    from configi import DynamicConfig, JSONConfigSource

    source = JSONConfigSource("https://some-url.com/my-config-file.json")
    config = DynamicConfig(
                    source,
                    expiry=(60*4),  # Every four hours reload
                    quiet_mode=True,  # Errors will `print` instead of throwing Exceptions.
                    namespace_dicts=True,  # Turn dictionaries into dot-accessible namespaces.
                    defaults={'some_key': 'a_value'}  # Defaults dict is used to return values, if a key is unset remotely.
                )

    print config.foo
        > None

    config.foo = 'bar'
        > DynamicConfigError: Could not set key foo



Caveats
-------

Some of the config sources are better suited for read-only config. Namely, the arbitrary-JSON-file-based config is strictly read-only. The S3-based config is read/write but not very optimal for high-write scenarios. Redis, if a Redis store is both secure and available to you, is probably your best bet.