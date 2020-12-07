#  Copyright (c) 2020 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.

from __future__ import annotations

import firefly as ff

import firefly_business_rules.domain as domain


@ff.command_handler()
class EvaluateRules(ff.ApplicationService):
    _registry: ff.Registry = None
    _engine: domain.RulesEngine = None

    def __call__(self, name: str, data: dict, stop_on_first_trigger: bool = False, **kwargs):
        for rule in list(self._registry(domain.RuleSet).filter(lambda rs: rs.name == name)):
            self._engine.evaluate_rule_set(rule, data, stop_on_first_trigger=stop_on_first_trigger)
