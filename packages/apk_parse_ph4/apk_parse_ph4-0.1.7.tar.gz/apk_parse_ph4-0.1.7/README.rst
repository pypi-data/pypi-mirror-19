APK parse
=========

-  reference `androguard <https://github.com/androguard/androguard>`__.
-  fork of `apk\_parse <https://github.com/tdoly/apk_parse>`__
-  partial support for xAPKs added (nested APKs)


Pip
===

::

    pip install apk_parse_ph4

Installation MacOS X
====================

If there are problems with installing ``m2crypto`` on Mac, try this:

::

    brew install openssl
    brew install swig
    env LDFLAGS="-L$(brew --prefix openssl)/lib" \
        CFLAGS="-I$(brew --prefix openssl)/include" \
        SWIG_FEATURES="-cpperraswarn -includeall -I$(brew --prefix openssl)/include" \
        pip install m2crypto

or

::

    LDFLAGS="-L/opt/local/lib" \
        CFLAGS="-I/opt/local/include" \
        SWIG_FEATURES="-cpperraswarn -includeall -I/opt/local/include" \
        pip install --user m2crypto

Example:
--------

::


        apkf = APK("myfile.apk")
        apkf = APK(read("myfile.apk"), raw=True)

Extended example:
-----------------

The following example processes APK in a separate call. `as_file_name` set to True causes the file is
not read whole to the memory, but it used as a file - ZIP module does seek if needed. In this way also
big (e.g., 1.5 GB) apks can be loaded. `temp_dir` option allows APK processor to use temporary dir, e.g.
for xapk format, where sub-APK needs to be parsed::


        apkf = APK(apk_path, process_now=False, process_file_types=False, as_file_name=True, temp_dir='/tmp')
        apkf.file_md5 = 'abcd0102037292'  # skips MD5 recomputing (if already computed during download)
        apkf.process()

package
~~~~~~~

Return the name of the package

::


        >>> apkf.package
        com.android.vending

        >>> apkf.get_package()
        com.android.vending

file\_md5
~~~~~~~~~

Return the file md5 of the apk

::


        >>> apkf.file_md5
        40bdd920a3a3d2acf432e3c5b485eb11

cert\_md5
~~~~~~~~~

Return the cert md5 of the apk

::


        >>> apkf.cert_md5
        cde9f6208d672b54b1dacc0b7029f5eb

file\_size
~~~~~~~~~~

Return the apk file size

::


        >>> apkf.file_size
        11194863

androidversion
~~~~~~~~~~~~~~

Return the apk version

::


        >>> apkf.androidversion
        {'Code': u'80341200', 'Name': u'5.4.12'}

get\_androidversion\_code()
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Return the android version code

::


        >>> apkf.get_androidversion_code()
        80341200

get\_androidversion\_name()
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Return the android version name

::


        >>> apkf.get_androidversion_name()
        5.4.12

get\_min\_sdk\_version()
~~~~~~~~~~~~~~~~~~~~~~~~

Return the android:minSdkVersion attribute

::


        >>> apkf.get_min_sdk_version()
        9

get\_target\_sdk\_version()
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Return the android:targetSdkVersion attribute

::


        >>> apkf.get_target_sdk_version()
        21

get\_libraries()
~~~~~~~~~~~~~~~~

Return the android:name attributes for libraries

::


        >>> apkf.get_libraries()
        []

get\_files()
~~~~~~~~~~~~

Return the files inside the APK

::


        >>> apkf.get_files()
        [u'AndroidManifest.xml', u'assets/keys/dcb-pin-encrypt-v1/1',...]

get\_files\_types()
~~~~~~~~~~~~~~~~~~~

Return the files inside the APK with their associated types (by using
python-magic) Please ``pip install python-magic``

::

        >>> apkf.get_files_types()
        {u'res/layout/play_card_bundle_item_small.xml': "Android's binary XML",...}

get\_main\_activity()
~~~~~~~~~~~~~~~~~~~~~

Return the name of the main activity

::


        >>> apkf.get_main_activity()
        com.android.vending.AssetBrowserActivity

get\_activities()
~~~~~~~~~~~~~~~~~

Return the android:name attribute of all activities

::


        >>> apkf.get_activities()
        ['com.android.vending.AssetBrowserActivity', ...]

get\_services()
~~~~~~~~~~~~~~~

Return the android:name attribute of all services

::


        >>> apkf.get_services()
        ['com.android.vending.GCMIntentService', ...]

get\_receivers()
~~~~~~~~~~~~~~~~

Return the android:name attribute of all receivers

::


        >>> apkf.get_receivers()
        ['com.google.android.gcm.GCMBroadcastReceiver', ...]

get\_providers()
~~~~~~~~~~~~~~~~

Return the android:name attribute of all providers

::


        >>> apkf.get_providers()
        ['com.google.android.finsky.providers.RecentSuggestionsProvider', ...]

get\_permissions()
~~~~~~~~~~~~~~~~~~

Return permissions

::


        >>> apkf.get_permissions()
        ['com.android.vending.permission.C2D_MESSAGE', ...]

show()
~~~~~~

Return FILES, PERMISSIONS, MAIN ACTIVITY...

::


        >>> apkf.show()
        FILES: ...

parse\_icon()
~~~~~~~~~~~~~

Parse ICON of the apk, storage on icon\_path

::


        >>> apkf.parse_icon(icon_path='/tmp')
        ...

cert\_text
~~~~~~~~~~

::


        >>> apkf.cert_text
        Certificate:
        Data:Version: 3 (0x2)
        ...

cert\_pem
~~~~~~~~~

::


        >>> apkf.cert_pem
        -----BEGIN CERTIFICATE-----
        ...


pkcs7\_der
~~~~~~~~~~

::


        >>> apkf.pkcs7_der
        (binary data)

