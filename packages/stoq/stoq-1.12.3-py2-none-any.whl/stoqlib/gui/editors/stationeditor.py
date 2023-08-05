# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2006 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##
""" Editor dialog for station objects """

from kiwi.datatypes import ValidationError

from stoqlib.api import api

from stoqlib.database.runtime import get_current_station
from stoqlib.domain.station import BranchStation
from stoqlib.domain.person import Branch
from stoqlib.gui.editors.baseeditor import BaseEditor
from stoqlib.lib.translation import stoqlib_gettext

_ = stoqlib_gettext


class StationEditor(BaseEditor):
    model_name = _('Computer')
    model_type = BranchStation
    gladefile = 'StationEditor'
    proxy_widgets = ('name', 'branch', 'is_active')

    #
    # BaseEditor Hooks
    #
    def __init__(self, store, model=None, visual_mode=False):
        BaseEditor.__init__(self, store, model, visual_mode)

        # do not let the user change the current station
        if model and get_current_station(store) == model:
            self.name.set_sensitive(False)
            self.is_active.set_sensitive(False)

        self.set_description(self.model.name)

    def create_model(self, store):
        return BranchStation(name=u"", branch=None,
                             is_active=True,
                             store=store)

    def setup_proxies(self):
        branches = self.store.find(Branch)
        self.branch.prefill(api.for_person_combo(branches))

        self.add_proxy(self.model, StationEditor.proxy_widgets)
        if not self.edit_mode:
            self.is_active.set_sensitive(False)

    def on_confirm(self):
        # FIXME: This is a hack, figure out why it's not set by the proxy
        self.model.branch = self.branch.get_selected_data()

    def on_name__validate(self, entry, value):
        if self.model.check_station_exists(value):
            msg = (_("There is already a station registered as `%s'.") %
                   value)
            return ValidationError(msg)
