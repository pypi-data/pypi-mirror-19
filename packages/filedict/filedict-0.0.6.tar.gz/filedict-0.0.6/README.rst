filedict
========


Purposes
--------

There are a lot of great in-memory key-value storages like Redis/Memcache. But
all of them are limited by RAM. Imagine you want to store 100,000,000,000 of
key-value pairs and have quite fast random-access to items by key. Filedict
was designed exactly for this case.


Install
-------
::

    $ git clone https://bitbucket.org/dkuryakin/filedict.git
    $ cd filedict && python setup.py install


or

::

    $ pip install filedict


Documentation
-------------

I believe that the best documentation - is a comprehensive and in-place
commented set of examples. So here they are:

.. code-block:: python

    import ctypes
    import filedict


    class Storage(filedict.BaseStorage):
        # This is simple in-file storage based on hash table.

        max_records = 1000
        # You can not save more than 1000 values in this database! This limit
        # can not be changed in the future. It is necessary to initially
        # correctly estimate the maximum number of entries in the database.
        # In the worst case it is necessary to copy this database to the new
        # larger database element by element.

        key_types = ctypes.c_uint64,
        val_types = ctypes.c_uint32, ctypes.c_uint32
        # Specify key & value binary representation. Each record in database
        # file has size = 1 + sizeof(key) + sizeof(val). In current case it's
        # 1 + 8 + (4 + 4) = 17 bytes. So resulting database file has size
        # 1000 * 17 = 17000 bytes. You can check this fact yourself. Note:
        # key-value types are fixed, and can't be changed in future!


    # Use simple try-finally form:
    db = Storage('/path/to/db', read_only=False, read_count=100)
    # There are 3 parameters when create instance of Storage: path, read_only
    # and read_count. Path - path to database dir. Only one writer per database
    # is allowed, so use read_only=True if you don't need any writes. Read
    # count specify read block size for all operations which involve a lot of
    # sequential reads. Default value for read_count is quite good for most of
    # cases.
    db.record_size == 1 + 8 + (4 + 4)  # True.
    try:
        db.open()
        # do something with db
    finally:
        db.close()


    # Or use context-manager form:
    with Storage('/path/to/db', read_only=False, read_count=100) as db:
        # You can add key-value pair to database. Return None. Duplicate keys
        # allowed. Duplicate key-value pairs allowed too.
        key1 = 0,
        key2 = 1,
        val1 = 0, 1
        val2 = 1, 2
        val3 = 2, 3
        db.add(key1, val1)
        db.add(key1, val2)
        db.add(key2, val3)
        # Note: this type of storage is rapidly becoming ineffective in the
        # case of a large number of records with the same key. So it is
        # recommended to take care of a high degree of uniqueness at the
        # application level. Besides the performance starts to drop
        # dramatically when free space ends in the database. It is recommended
        # to set value of max_records 10-15% more than the actual maximum
        # size of the database. Also writes slow down on SATA disks for huge
        # databases. If you want to store huge amount of data and you don't
        # have SSD disk - try to use BaseShardedStorage instead (see below).

        # You can iterate over different values for target key.
        it = db.values(key1)  # Return generator.
        set(it) == set([val1, val2])  # Sets are equal, but iteration order is
                                      # not defined!

        # You can iterate over all key-value pairs in database. Note: order is
        # not defined!
        it = db.items()  # Returns generator.
        set(it) == set([(key1, val1), (key1, val2), (key2, val3)])

        # You can get estimation for database size. Note: this estimation is
        # precise for writer. It can be outdated for readers in case of active
        # writer. But if there is no active writer, estimation will be precise
        # for readers too.
        len(db) == 3  # That's True.

        # It's possible to delete all mentions of key-value pair from database.
        1 == db.del_value(key1, val1)  # Return number of deleted records.
        len(db) == 2  # True.
        db.deleted_count == 1  # True.

        # We also can delete all records with target key.
        1 == db.del_key(key1)  # Return number of deleted records.
        len(db) == 1  # True.
        db.deleted_count == 2  # True.

        # After set of add-del operations database can come to not optimized
        # state. We can fix it in-place:
        db.defragmentation()
        db.deleted_count == 0  # True. All "voids" are optimized.
        # Note: this is VERY heavy operation. Use it only at worst case.

        # len(db) & db.deleted_count - are kind of estimations. If server is
        # hung or shut down suddenly - these estimations may deviate from the
        # actual values. In that case we can fix it by following way:
        db.fix_statistis()
        # Note: this is really SLOW operation. Use it as seldom as possible.

        # You can create defragmented copy of database:
        db.copy('/path/to/db-copy', read_count=100)
        # Read count - read_count parameter passed to constructor of created
        # database. Note: this is VERY heavy operation!

        # And finally, you can copy database content to another storage:
        class ExtendedStorage(Storage):
            max_records = 2000
        with ExtendedStorage('/path/to/extended-db-copy') as edb:
            db.copy_to_storage(edb)
            len(db) == len(edb)  # True.
            set(db.items()) == set(edb.items())  # True.

    # Congratulations! Now you know everything about filedict.BaseStorage. But
    # there is one more component: filedict.BaseShardedStorage:
    class Storage(filedict.BaseShardedStorage):
        # It has some familiar parameters:
        max_records = 1000
        key_types = ctypes.c_uint64,
        val_types = ctypes.c_uint32, ctypes.c_uint32

        # And some new parameters:

        shard_name_width = 5
        # Length of shards names. In case of 3, shard names will be: 00000,
        # 00001, 00002, .. etc. Default value is good for most of cases.

        max_shard_fulness = 0.9
        # Maximum allowed fulness of each shard subdatabase. Default value is
        # good for most of cases.

        # It's worth noting that sharded storage has no limitation for maximum
        # number of records in database. Value of max_records - is just a
        # limitation for single shard. And there is no limits for shards count.
        # But this feature leads to changes in performance balance. First,
        # ALL reads are slowed SHARDS_COUNT times (both SATA & SSD). Second,
        # writes on SATA are not slowed if use max_records =
        # (RAM_SIZE - RAM_SIZE_USED_BY_OS) / (1 + sizeof(key) + sizeof(val)).

        # For example, we have SATA and 16Gb of RAM. And 4Gb are permanently
        # used by OS and some applications. In this case, recommended
        # value for max_records is:
        # (16 - 4)*1024*1024*1024 / (1 + 8 + (4 + 4)) ~ 750,000,000
        # So, set max_records to 750000000 and obtain fast writes!

        # If you have SSD - just use BaseStorage!

    # Now let's consider possible exceptions.
    try:
        # create database object, open it and perform some operations.
    except filedict.WrongFileSizeError:
        # Will be raised if change max_records for existing database.
    except filedict.UnableToSeekError:
        # Will be raised if try to seek to position that is greater than file
        # size.
    except filedict.UnableToReadError:
        # Will be raised if can not read from database file.
    except filedict.UnableToWriteError:
        # Will be raised if can not write to database file.
    except filedict.UnableToWriteRawError:
        # Will be raised if can not write raw data to database file.
    except filedict.RequiredAttrNotExistsError:
        # Will be raised if some of required params are not specified (for
        # example max_records).
    except filedict.WriteInReadOnlyModeError:
        # Will be raised if try to perform write operation for read-only opened
        # database.
    except filedict.StorageIsFullError:
        # Will be raised if try to add item in full database.
    except filedict.CopyAlreadyExistsError:
        # Will be raised if try to copy database to path that already exists.
    except filedict.NotOpenedError:
        # Will be raised if try to perform some operation on database that was
        # not opened.

    # Note:
    # StorageFileError - is base class for WrongFileSizeError,
    # UnableToSeekError, UnableToReadError, UnableToWriteError,
    # UnableToWriteRawError.
    # BaseStorageError - base class for RequiredAttrNotExistsError,
    # WriteInReadOnlyModeError, StorageIsFullError, CopyAlreadyExistsError,
    # NotOpenedError


Features
--------

 - Simple in-file hash table.
 - Can store billions of records providing really fast access.
 - Use disk space effectively.
 - Use a little bit RAM.
 - Support both add & del operations.
 - Support defragmentation, copy operation.
 - No limits to readers number.
 - Support multiple values for single key.
 - Get value for given key only in 1 seek + 1 read (in best case, if keys are quite unique).
 - Supports local sharding.


Limitations
-----------

 - Only python2, only linux for now.
 - Max number of records is constant for any database. So it can be choosen only once.
 - Supports only fixed data schema.
 - Can store only integers & floats.
 - Very slow in case of huge amount of duplicate keys.
 - Only one writer allowed.
 - No transactions, no ACID support.
 - If your data can be placed in RAM, use Redis/Memcache instead!
 - Not distributed.


Tests
-----

Very simple, just run:
::

    $ git clone https://bitbucket.org/dkuryakin/filedict.git
    $ cd filedict && python setup.py test


or

::

    $ python -mfiledict.test


Changelog
---------

https://bitbucket.org/dkuryakin/filedict/raw/master/CHANGES.txt


License
-------

::

    This is free and unencumbered software released into the public domain.

    Anyone is free to copy, modify, publish, use, compile, sell, or
    distribute this software, either in source code form or as a compiled
    binary, for any purpose, commercial or non-commercial, and by any
    means.

    In jurisdictions that recognize copyright laws, the author or authors
    of this software dedicate any and all copyright interest in the
    software to the public domain. We make this dedication for the benefit
    of the public at large and to the detriment of our heirs and
    successors. We intend this dedication to be an overt act of
    relinquishment in perpetuity of all present and future rights to this
    software under copyright law.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
    OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

    For more information, please refer to <http://unlicense.org/>
