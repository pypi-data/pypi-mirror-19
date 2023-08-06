"""PytSite MetaTag Module.
"""
from ._api import dump, dump_all, get, reset, t_set, rm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang, events, tpl

    lang.register_package(__name__)
    events.listen('pytsite.router.dispatch', reset)

    tpl.register_global('metatag', dump)
    tpl.register_global('metatags', dump_all)
    tpl.register_global('metatag_get', get)


_init()
