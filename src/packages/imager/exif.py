#-*- coding: utf-8 -*-
# exif.py  (c)2021  Henrique Moreira

"""
Classes for EXIF (image information).

Wrappers for Pillow (Python PIL):
- see also https://pillow.readthedocs.io/
"""

# pylint: disable=missing-function-docstring

import PIL.Image
import PIL.ExifTags

TYPICAL_EXCLUDE = (
    "MakerNote",
    "ImageUniqueID",
    "PrintImageMatching",	# e.g. b'PrintIM\x000250\x00...\x00\x00\x00\x00
    "ComponentsConfiguration",	# e.g. b'\x01\x02\x03\x00'
)
#	ExifVersion': b'0220',
#	'ComponentsConfiguration': b'\x01\x02\x03\x00'

EXCUDE_STR = "---"


def hints(fname:str, excl=None) -> dict:
    """ Returns the raw EXIF tags.
    This method is quite un-optimized, but allows you to get an idea of how
    EXIF indexing works.
    """
    # pylint: disable=protected-access
    exclude = excl if excl else TYPICAL_EXCLUDE
    assert isinstance(exclude, (tuple, list))
    img = PIL.Image.open(fname)
    #	PIL.ExifTags.TAGS[k]: value ... if k in PIL.ExifTags.TAGS
    there = img._getexif()
    if not there:
        return dict()
    exifs = {
        what_tag(k): value if what_tag(k) not in TYPICAL_EXCLUDE else EXCUDE_STR
        for k, value in there.items()
        if what_tag(k) is not None
    }
    exifs['@version'] = get_version(exifs.get('ExifVersion'))
    return exifs

def what_tag(key:int):
    assert isinstance(key, int)
    res = PIL.ExifTags.TAGS.get(key)
    # returns None if 'key' integer is not in TAGS
    return res

def get_version(exif_version):
    """ See: exifs['ExifVersion']
    Reference: https://www.metadata2go.com/file-info/exif-version
    """
    if not exif_version:
        return "unknown"
    assert len(exif_version) == 4, f"Unexpected exif_version: {exif_version}"
    assert isinstance(exif_version, bytes)
    xyz = exif_version
    astr = xyz.decode("ascii")
    if len(astr) < 4:
        return "?"
    result = astr[:2] + "." + astr[2] + '.' + astr[3]
    if result[0] == "0" and result.rstrip(".0") != result:
        return result[1:].rstrip(".0")	# return 2.2 or 2.3, usually
    return result

def iso_dot_date(astr:str):
    assert isinstance(astr, str)
    park = astr.split(" ", maxsplit=1)
    return park[0].replace(":", ".") + " " + park[1]


# Main script
if __name__ == "__main__":
    print("Please import me.")
