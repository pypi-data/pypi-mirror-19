# -*- coding: utf-8 -*-
"""A fastavro-based avro reader for Dask.

Disclaimer: The initial code was recovered from dask's distributed project.

"""
import io
import fastavro
import json

from dask import delayed
from dask.bytes import read_bytes
from dask.bytes.core import OpenFileCreator


__author__ = 'Rolando (Max) Espinoza'
__email__ = 'rolando at rmax.io'
__version__ = '0.1.0'


def read_avro(urlpath, blocksize=2**27, **kwargs):
    """Reads avro files.

    Parameters
    ----------
    urlpath : string
        Absolute or relative filepath, URL or globstring pointing to avro files.
    blocksize : int, optional
        Size of blocks. Default is 128MB.
    **kwargs
        Additional arguments passed to ``dask.bytes.read_bytes`` function.

    Returns
    -------
    out : list[Delayed]
        A list of delayed objects, one for each block.

    """
    myopen = OpenFileCreator(urlpath)
    values = []
    for fn in myopen.fs.glob(urlpath):
        with myopen(fn) as fp:
            av = fastavro.reader(fp)
            header = av._header
        _, blockss = read_bytes(fn, delimiter=header['sync'], not_zero=True,
                                sample=False, blocksize=blocksize, **kwargs)
        values.extend(
            delayed(_avro_body)(block, header) for blocks in blockss for block in blocks
        )
    if not values:
        raise ValueError("urlpath is empty: %s" % urlpath)

    return values


def _avro_body(data, header):
    """Returns records for given avro data fragment."""
    stream = io.BytesIO(data)
    schema = json.loads(header['meta']['avro.schema'].decode())
    codec = header['meta']['avro.codec'].decode()
    return iter(fastavro._reader._iter_avro(stream, header, codec, schema, schema))
