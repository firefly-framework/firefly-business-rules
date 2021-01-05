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

import json
from typing import Callable, Union

import business_rules.actions as bra
import business_rules.variables as brv
import firefly as ff
from business_rules import run_all
from business_rules.fields import FIELD_TEXT

import firefly_business_rules.domain as domain
from firefly_business_rules.domain.entity.rule_set import RuleSet


class VenmoRulesEngine(domain.RulesEngine, ff.SystemBusAware):
    _variable_objects: dict = {}
    _action_object: type = None
    _rule_sets: dict = {}

    def evaluate_rule_set(self, rule_set: RuleSet, data: dict, stop_on_first_trigger: bool = True):
        variables = self._build_variables_object(data)
        actions = self._build_action_object()

        run_all(
            rule_list=self._generate_rules(rule_set),
            defined_variables=variables(data),
            defined_actions=actions(data),
            stop_on_first_trigger=stop_on_first_trigger
        )

    def _build_variables_object(self, input_data: dict):
        key = json.dumps(list(input_data.keys()))
        if key in self._variable_objects:
            return self._variable_objects[key]

        class Variables(brv.BaseVariables):
            def __init__(self, data: dict):
                self.data = data

        for key, variable in input_data.items():
            if isinstance(variable, (int, float)):
                self._add_property_getter(Variables, key, brv.numeric_rule_variable)
            elif isinstance(variable, bool):
                self._add_property_getter(Variables, key, brv.boolean_rule_variable)
            else:
                self._add_property_getter(Variables, key, brv.string_rule_variable)

        self._variable_objects[key] = Variables

        return Variables

    @staticmethod
    def _add_property_getter(cls, name: str, variable_type: Callable, options: list = None):
        def inner(self):
            return self.data[name]
        inner.__name__ = name
        if options is not None:
            setattr(cls, name, variable_type(inner, options=options))
        else:
            setattr(cls, name, variable_type(inner))

    def _build_action_object(self):
        if self._action_object is not None:
            return self._action_object

        class Actions(bra.BaseActions):
            _system_bus: ff.SystemBus = None

            def __init__(self, data: dict):
                self.data = data

            @bra.rule_action(params={'command': FIELD_TEXT})
            def invoke_command(self, command: str):
                self._system_bus.invoke(command, self.data)

        Actions._system_bus = self._system_bus
        self._action_object = Actions

        return Actions

    def _generate_rules(self, rule_set: domain.RuleSet):
        if rule_set.id in self._rule_sets:
            return self._rule_sets[rule_set.id]

        ret = []

        for rule in rule_set.rules:
            x = {'conditions': self._do_generate_rules(rule.conditions), 'actions': []}
            for cmd in rule.commands:
                x['actions'].append({
                    'name': 'invoke_command',
                    'params': {
                        'command': cmd.name
                    }
                })
            ret.append(x)

        self._rule_sets[rule_set.id] = ret

        return ret

    def _do_generate_rules(self, conditions: domain.ConditionSet):
        ret = {}

        key = 'any'
        if conditions.all is True:
            key = 'all'
        ret[key] = []

        for condition in conditions.conditions:
            ret[key].append({'name': condition.name, 'operator': condition.operator, 'value': condition.value})
        for condition in conditions.sub_conditions:
            ret[key].append(self._do_generate_rules(condition))

        return ret
