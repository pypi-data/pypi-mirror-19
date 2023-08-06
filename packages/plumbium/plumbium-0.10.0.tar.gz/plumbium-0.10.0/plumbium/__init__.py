"""plumbium is a module for recording the activity of file processing pipelines.

.. moduleauthor:: Jon Stutters <j.stutters@ucl.ac.uk>
"""

from pkg_resources import resource_string
from .processresult import pipeline, record, call


__version__ = resource_string(__name__, 'VERSION').strip()
__all__ = ('pipeline', 'record', 'call')
