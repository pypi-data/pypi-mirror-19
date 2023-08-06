#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import binascii
from apk_parse.apk import APK


def test():
    if len(sys.argv) == 1:
        print('Usage: %s app.apk' % sys.argv[0])
        sys.exit(1)

    apk_path = sys.argv[1]

    # Parsing xapks.
    apkf = APK(apk_path, process_now=False, process_file_types=False, as_file_name=True)
    apkf.file_md5 = 'skip'
    apkf.process()

    print(apkf.file_md5)
    print(apkf.file_size)
    print(apkf.cert_md5)
    print(apkf.cert_text)
    print(apkf.cert_pem)


if __name__ == "__main__":
    test()