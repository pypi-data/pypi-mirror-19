"""Settings Plugin Endpoints
"""
import re as _re
from pytsite import auth as _auth, metatag as _metatag, lang as _lang, router as _router, http as _http, \
    admin as _admin, util as _util
from . import _api, _frm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _build_form(setting_uid: str) -> _frm.Form:
    """Internal helper.
    """
    # Load setting definition
    setting_def = _api.get_definition(setting_uid)

    return setting_def['form']('settings-form', setting_uid=setting_uid)  # type: _frm.Form


def form(args: dict, inp: dict) -> str:
    """Render settings form.
    """
    uid = args.get('uid')

    if not _check_permissions(uid):
        raise _http.error.Forbidden()

    # Load setting definition
    setting_def = _api.get_definition(uid)

    # Update page's title
    _metatag.t_set('title', _lang.t(setting_def['title']))

    # Instantiate form
    frm = _build_form(uid)

    return _admin.render_form(frm)


def form_submit(args: dict, inp: dict) -> _http.response.Redirect:
    """Process settings form submit.
    """
    uid = args.get('uid')
    if not _check_permissions(uid):
        raise _http.error.Forbidden()

    frm = _build_form(uid).fill(inp)

    # We'll process ALL input, not only form's widgets, because widgets can be added by JS on client side
    inp_values = _util.dict_merge(dict(frm.values), inp)

    setting_value = {}
    for k, v in inp_values.items():
        if k.startswith('setting_'):
            k = _re.sub('^setting_', '', k)

            if isinstance(v, (list, tuple)):
                v = _util.cleanup_list(v)

            if isinstance(v, dict):
                v = _util.cleanup_dict(v)

            setting_value[k] = v

    _api.put(uid, _util.dict_merge(_api.get(uid), setting_value))

    frm.submit()

    _router.session().add_success_message(_lang.t('pytsite.settings@settings_has_been_saved'))

    return _http.response.Redirect(_router.ep_url('pytsite.settings@form', {'uid': uid}))


def _check_permissions(uid: str) -> bool:
    section_def = _api.get_definition(uid)
    if section_def['perm_name'] == '*':
        return True

    return _auth.get_current_user().has_permission(section_def['perm_name'])
