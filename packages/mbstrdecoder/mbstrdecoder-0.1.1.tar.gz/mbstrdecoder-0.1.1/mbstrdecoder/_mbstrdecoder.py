# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import re
import sys

import six


class MultiByteStrDecoder(object):
    __CODEC_LIST = (
        'utf_7',
        'utf_8', 'utf_8_sig',
        'utf_16', 'utf_16_be', 'utf_16_le',
        'utf_32', 'utf_32_be', 'utf_32_le',

        'big5', 'big5hkscs',
        'cp037', 'cp424', 'cp437', 'cp500', 'cp720',
        'cp737', 'cp775', 'cp850', 'cp852', 'cp855',
        'cp856', 'cp857', 'cp858', 'cp860', 'cp861',
        'cp862', 'cp863', 'cp864', 'cp865', 'cp866',
        'cp869', 'cp874', 'cp875', 'cp932', 'cp949',
        'cp950', 'cp1006', 'cp1026', 'cp1140', 'cp1250',
        'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255',
        'cp1256', 'cp1257', 'cp1258',
        'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr',
        'gb2312', 'gbk', 'gb18030',
        'hz',
        'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004',
        'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr',
        'latin_1',
        'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6',
        'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_11',
        'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16',
        'johab',
        'koi8_r', 'koi8_u',
        'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish',
        'ptcp154',
        'shift_jis', 'shift_jis_2004', 'shift_jisx0213',
    )

    __RE_UTF7 = re.compile(six.b("[+].*?[-]"))

    @property
    def unicode_str(self):
        return self.__unicode_str

    @property
    def codec(self):
        return self.__codec

    def __init__(self, value):
        self.__encoded_str = value
        self.__codec = None

        self.__unicode_str = self.__to_unicode()

    def __is_buffer(self):
        if sys.version_info.major <= 2:
            return isinstance(self.__encoded_str, buffer)

        return isinstance(self.__encoded_str, memoryview)

    def __is_multibyte_utf7(self, encoded_str):
        if self.__codec != "utf_7":
            return False

        utf7_symbol_count = encoded_str.count(six.b("+"))
        if utf7_symbol_count <= 0:
            return False

        if utf7_symbol_count != encoded_str.count(six.b("-")):
            return False

        return utf7_symbol_count == len(self.__RE_UTF7.findall(encoded_str))

    def __get_encoded_str(self):
        if self.__is_buffer():
            return str(self.__encoded_str)

        return self.__encoded_str

    def __to_unicode(self):
        encoded_str = self.__get_encoded_str()

        for codec in self.__CODEC_LIST:
            try:
                self.__codec = codec
                decoded_str = encoded_str.decode(codec)
                break
            except UnicodeDecodeError:
                continue
            except UnicodeEncodeError:
                # already a unicode string
                return encoded_str
            except AttributeError:
                try:
                    return "{}".format(encoded_str)
                except UnicodeDecodeError:
                    # some of the objects that cannot convertible to a string
                    # may reach this line
                    raise TypeError("argument must be a string")
        else:
            self.__codec = None

            try:
                message = "unknown codec: encoded_str={}".format(encoded_str)
            except UnicodeDecodeError:
                message = "unknown codec: value-type={}".format(
                    type(encoded_str))

            raise UnicodeDecodeError(message)

        if self.codec == "utf_7":
            if self.__is_multibyte_utf7(encoded_str):
                try:
                    _work = decoded_str.encode("ascii")

                    self.__codec = "ascii"
                    decoded_str = encoded_str.decode("ascii")
                except UnicodeEncodeError:
                    pass
            else:
                self.__codec = "ascii"
                decoded_str = encoded_str.decode("ascii")

        return decoded_str
