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

import business_rules.variables as brv

import firefly_business_rules.domain as domain
from firefly_business_rules.domain.entity.input import Input
from firefly_business_rules.domain.entity.rule_set import RuleSet


class VenmoRulesEngine(domain.RulesEngine):
    _variable_objects: dict = {}

    def evaluate_rule_set(self, rule_set: RuleSet, input_: Input):
        pass

    def _build_variables_object(self, input_: Input):
        if input_.id in self._variable_objects:
            return self._variable_objects[input_.id]

        class Variables(brv.BaseVariables):
            def __init__(self, data: dict):
                self.data = data

        for variable in input_.variables:
            def var(self):
                return self.data[variable.name]
            if variable.type == 'string':
                var = brv.string_rule_variable(var)
            elif variable.type == 'number':
                var = brv.numeric_rule_variable(var)
            elif variable.type == 'boolean':
                var = brv.boolean_rule_variable(var)
            elif variable.type == 'select':
                var = brv.select_rule_variable(var, options=variable.options)
            elif variable.type == 'select-multiple':
                var = brv.select_multiple_rule_variable(var, options=variable.options)

            setattr(Variables, variable.name, var)

        self._variable_objects[input_.id] = Variables

        return Variables
