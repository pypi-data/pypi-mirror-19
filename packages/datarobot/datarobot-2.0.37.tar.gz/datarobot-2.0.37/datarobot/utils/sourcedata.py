import os

import pandas as pd
import six

import datarobot.errors as errors


def dataframe_to_buffer(df):
    """Convert a dataframe to a serialized form in a buffer

    Parameters
    ----------
    df : pandas.DataFrame
        The data to serialize

    Returns
    -------
    buff : StringIO()
        The data. The descriptor will be reset before being returned (seek(0))
    """
    buff = six.StringIO()
    df.to_csv(buff, encoding='utf-8', index=False)
    buff.seek(0)
    return buff


def is_urlsource(sourcedata):
    """ Whether sourcedata is of url kind
    """
    return isinstance(sourcedata, six.string_types) and sourcedata.startswith('http')


def recognize_sourcedata(sourcedata, default_fname):
    """Given a sourcedata figure out if it is a filepath, dataframe, or
    filehandle, and then return the correct kwargs for the upload process
    """
    if isinstance(sourcedata, pd.DataFrame):
        buff = dataframe_to_buffer(sourcedata)
        return {'filelike': buff,
                'fname': default_fname}
    elif hasattr(sourcedata, 'read') and hasattr(sourcedata, 'seek'):
        return {'filelike': sourcedata,
                'fname': default_fname}
    elif isinstance(sourcedata, six.string_types) and os.path.isfile(sourcedata):
        file_basename = os.path.basename(sourcedata)
        try:
            file_basename.encode('ascii')
        # Which exception we get here depends on whether the input was string or unicode
        # (we allow both)
        except (UnicodeEncodeError, UnicodeDecodeError):
            raise errors.IllegalFileName
        return {'file_path': sourcedata,
                'fname': file_basename}
    elif isinstance(sourcedata, six.binary_type) and not is_urlsource(sourcedata):
        return {'content': sourcedata,
                'fname': default_fname}
