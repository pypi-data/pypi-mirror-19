# -*- coding: utf-8 -*-

"""
Created on 2017-01-03
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from kotti.views.slots import assign_slot
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_history')

controlpanel_id = "kotti_history"


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_history.kotti_configure

        to enable the ``kotti_history`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_history'
    settings['kotti.populators'] += ' kotti_history.populate.populate'
    settings['kotti.alembic_dirs'] += ' kotti_history:alembic'
    settings['kotti.fanstatic.view_needed'] += ' kotti_history.fanstatic.css_and_js'
    assign_slot('history-recorder', 'belowcontent')


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_translation_dirs('kotti_history:locale')
    config.add_static_view('static-kotti_history', 'kotti_history:static')

    config.scan(__name__)
