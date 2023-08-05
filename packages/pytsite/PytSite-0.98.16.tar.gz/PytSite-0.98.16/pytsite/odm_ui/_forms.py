"""PytSite ODM Entity Modify Form.
"""
from pytsite import form as _form, widget as _widget, lang as _lang, http as _http, odm as _odm, events as _events, \
    metatag as _metatag, router as _router, html as _html, odm_auth as _odm_auth
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Modify(_form.Form):
    def __init__(self, uid: str = None, **kwargs):
        """Init.
        """
        self._model = kwargs.get('model')
        if not self._model:
            raise ValueError('Model is not specified.')

        self._eid = kwargs.get('eid')
        self._update_meta_title = kwargs.get('update_meta_title', True)

        super().__init__(uid, **kwargs)

    @property
    def update_meta_title(self) -> bool:
        return self._update_meta_title

    @update_meta_title.setter
    def update_meta_title(self, value: bool):
        self._update_meta_title = value

    def _setup_form(self, **kwargs):
        """Hook.
        :param **kwargs:
        """
        from ._api import dispense_entity

        try:
            entity = dispense_entity(self._model, self._eid)
        except _odm.error.EntityNotFound:
            raise _http.error.NotFound()

        # Check if entities of this model can be created
        if not self._eid and not entity.check_permissions('create'):
            raise _http.error.Forbidden()

        # Check if the entity can be modified
        if self._eid and not entity.check_permissions('modify'):
            raise _http.error.Forbidden()

        # Form title
        if entity.is_new:
            self._title = entity.t('odm_ui_form_title_create_' + self._model)
        else:
            self._title = entity.t('odm_ui_form_title_modify_' + self._model)

        # Setting up the form through entity hook and global event
        entity.odm_ui_m_form_setup(self)
        _events.fire('pytsite.odm_ui.{}.m_form_setup'.format(self._model), frm=self, entity=entity)

        if self._update_meta_title:
            _metatag.t_set('title', self.title)

        # Default redirect
        if not self._redirect:
            self._redirect = 'ENTITY_VIEW'

        # Action URL
        self._action = _router.ep_url('pytsite.odm_ui@m_form_submit', {
            'model': self._model,
            'id': self._eid or '0',
        })

        # CSS
        self.css += ' odm-ui-form odm-ui-form-' + self._model

    def _setup_widgets(self):
        from ._api import dispense_entity

        # Setting up form's widgets through entity hook and global event
        entity = dispense_entity(self._model, self._eid)
        entity.odm_ui_m_form_setup_widgets(self)
        _events.fire('pytsite.odm_ui.{}.m_form_setup_widgets'.format(self._model), frm=self, entity=entity)

        # Cancel button
        cancel_href = '#'
        if not self.modal:
            cancel_href = _router.request().inp.get('__redirect')
            if not cancel_href or cancel_href == 'ENTITY_VIEW':
                if not entity.is_new and entity.odm_ui_view_url():
                    cancel_href = entity.odm_ui_view_url()
                else:
                    cancel_href = _router.base_url()

        self.add_widget(_widget.button.Link(
            weight=10,
            uid='action-cancel',
            value=_lang.t('pytsite.odm_ui@cancel'),
            icon='fa fa-fw fa-remove',
            href=cancel_href,
            dismiss='modal',
            form_area='footer',
        ))

    def validate(self):
        # Perform native form validation
        super().validate()

        # Ask entity to validate the form
        from ._api import dispense_entity
        entity = dispense_entity(self._model, self._eid)
        entity.odm_ui_m_form_validate(self)


class MassAction(_form.Form):
    """ODM UI Mass Action Form.
    """

    def __init__(self, uid: str = None, **kwargs):
        """Init.
        """
        self._model = kwargs.get('model')
        if not self._model:
            raise ValueError('Model is not specified.')

        self._eids = kwargs.get('eids')
        if isinstance(self._eids, str):
            self._eids = self._eids.split(',')

        super().__init__(uid, **kwargs)

    def _setup_form(self, **kwargs):
        """Hook.
        :param **kwargs:
        """
        if not self._redirect:
            self._redirect = _router.ep_url('pytsite.odm_ui@browse', {'model': self._model})

    def _setup_widgets(self):
        """Hook.
        """
        from ._api import dispense_entity

        # List of items to process
        ol = _html.Ol()
        for eid in self._eids:
            entity = dispense_entity(self._model, eid)
            self.add_widget(_widget.input.Hidden(uid='ids-' + eid, name='ids', value=eid))
            ol.append(_html.Li(entity.odm_ui_mass_action_entity_description()))
        self.add_widget(_widget.static.HTML(uid='ids-text', em=ol))

        # Submit button
        submit_button = self.get_widget('action-submit')  # type: _widget.button.Submit
        submit_button.value = _lang.t('pytsite.odm_ui@continue')
        submit_button.icon = 'angle-double-right'

        # Cancel button
        self.add_widget(_widget.button.Link(
            uid='action-cancel',
            weight=10,
            value=_lang.t('pytsite.odm_ui@cancel'),
            href=self.redirect,
            icon='fa fa-fw fa-ban',
            form_area='footer'
        ))


class Delete(MassAction):
    """Entities Delete Form.
    """

    def _setup_form(self, **kwargs):
        """Hook.
        :param **kwargs:
        """
        super()._setup_form()

        # Check permissions
        if not _odm_auth.check_permissions('delete', self._model, self._eids):
            raise _http.error.Forbidden()

        # Action URL
        self._action = _router.ep_url('pytsite.odm_ui@d_form_submit', {'model': self._model})

        # Page title
        model_class = _odm.get_model_class(self._model)  # type: _model.UIEntity
        _metatag.t_set('title', model_class.t('odm_ui_form_title_delete_' + self._model))

    def _setup_widgets(self):
        """Hook.
        """
        super()._setup_widgets()

        # Change submit button color
        self.get_widget('action-submit').color = 'danger'
