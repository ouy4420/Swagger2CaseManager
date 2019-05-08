from io import BytesIO
from gzip import GzipFile
import jsonpickle
import sqlalchemy.types as types


def compress_string(s):
    zbuf = BytesIO()
    with GzipFile(mode='wb', compresslevel=6, fileobj=zbuf, mtime=0) as zfile:
        zfile.write(s)
    return zbuf.getvalue()


def uncompress_string(s):
    """helper function to reverse text.compress_string"""
    import base64
    import io
    import gzip
    try:
        val = base64.b64decode(s)
        zbuf = BytesIO(val)
        zfile = gzip.GzipFile(fileobj=zbuf)
        ret = zfile.read()
        zfile.close()
    except Exception as e:
        print(e)
        ret = s
    return ret


class CompressField(types.TypeDecorator):
    impl = types.Unicode

    def process_bind_param(self, value, engine):
        import base64
        if value:
            value = value.encode('utf8')
            value = compress_string(value)
            value = base64.b64encode(value).decode('utf8')
        return value
        # return unicode(jsonpickle.encode(value))

    def process_result_value(self, value, engine):
        if value:
            # return jsonpickle.decode(value)
            return uncompress_string(value).decode('utf8')
        else:
            # default can also be a list
            return '[]'


