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

import pytest

import firefly_business_rules.domain as domain
from firefly_business_rules.application.container import Container
from firefly_business_rules.infrastructure import VenmoRulesEngine


def test_integer_strings_are_cast_properly(sut: VenmoRulesEngine, rules):
    rule_set = rules([
        {
            'name': 'numeric_value',
            'value': '10000',
            'operator': 'greater_than_or_equal_to'
        }
    ])

    sut.evaluate_rule_set(rule_set, {'numeric_value': 10000})
    assert sut._system_bus.invoke.call_count == 1
    args, _ = sut._system_bus.invoke.call_args
    assert args[1]['custom'] == 'param'

    sut.evaluate_rule_set(rule_set, {'numeric_value': '10000'})
    assert sut._system_bus.invoke.call_count == 2


def test_float_strings_are_cast_properly(sut: VenmoRulesEngine, rules):
    rule_set = rules([
        {
            'name': 'float_value',
            'value': '10000.1',
            'operator': 'greater_than_or_equal_to'
        }
    ])

    sut.evaluate_rule_set(rule_set, {'float_value': 10000.2})
    assert sut._system_bus.invoke.call_count == 1

    sut.evaluate_rule_set(rule_set, {'float_value': '10001.1'})
    assert sut._system_bus.invoke.call_count == 2


def test_iso_format_dates(sut: VenmoRulesEngine, rules):
    rule_set = rules([
        {
            'name': 'date_value',
            'value': '2021-01-08T04:49:35.513374',
            'operator': 'greater_than'
        }
    ])

    sut.evaluate_rule_set(rule_set, {'date_value': '2021-01-08T04:49:36.513374'})
    assert sut._system_bus.invoke.call_count == 1

    sut.evaluate_rule_set(rule_set, {'date_value': '2021-01-07T04:49:36.513374'})
    assert sut._system_bus.invoke.call_count == 1


def test_list_contains(sut: VenmoRulesEngine, rules):
    rule_set = rules([
        {
            'name': 'list_value',
            'value': 'b',
            'operator': 'contains'
        }
    ])

    sut.evaluate_rule_set(rule_set, {'list_value': ['a', 'b', 'c']})
    assert sut._system_bus.invoke.call_count == 1

    sut.evaluate_rule_set(rule_set, {'list_value': ['a', 'c']})
    assert sut._system_bus.invoke.call_count == 1

    sut.evaluate_rule_set(rule_set, {'list_value': ['b', 'c']})
    assert sut._system_bus.invoke.call_count == 2


def test_list_contains_all(sut: VenmoRulesEngine, rules):
    rule_set = rules([
        {
            'name': 'list_value',
            'value': ['a', 'b'],
            'operator': 'contains_all'
        }
    ])

    sut.evaluate_rule_set(rule_set, {'list_value': ['a', 'b', 'c']})
    assert sut._system_bus.invoke.call_count == 1


def test_string_contains(sut: VenmoRulesEngine, rules):
    rule_set = rules([
        {
            'name': 'string_value',
            'value': 'foo',
            'operator': 'contains'
        }
    ])

    sut.evaluate_rule_set(rule_set, {'string_value': 'foobar'})
    assert sut._system_bus.invoke.call_count == 1


@pytest.fixture()
def sut():
    sut = Container().mock(VenmoRulesEngine)
    sut._action_object = None
    sut._system_bus.reset_mock()
    return sut


@pytest.fixture()
def rules():
    def build_rules(conditions: list):
        return domain.RuleSet.from_dict({
            'rules': [
                {
                    'commands': [
                        {
                            'id': 'ad7a1552-aa44-42d8-9d50-bd81a1e47aa0',
                            'name': 'foo.TakeAction',
                            'params': {'custom': 'param'}
                        }
                    ],
                    'conditions': {
                        'all': True,
                        'conditions': conditions
                    }
                }
            ]
        })

    return build_rules
