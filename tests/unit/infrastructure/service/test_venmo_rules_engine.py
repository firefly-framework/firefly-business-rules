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
from firefly_business_rules.infrastructure import VenmoRulesEngine
import firefly_business_rules.domain as domain

from firefly_business_rules.application.container import Container


def test_numbers(sut: VenmoRulesEngine, rules):
    sut.evaluate_rule_set(rules, {
        'numeric_value': 10000,
    })

    assert sut._system_bus.invoke.call_count == 1
    args, _ = sut._system_bus.invoke.call_args
    assert args[1]['custom'] == 'param'


@pytest.fixture()
def sut():
    sut = Container().mock(VenmoRulesEngine)
    sut._action_object = None
    return sut


@pytest.fixture()
def rules():
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
                    'conditions': [
                        {
                            'name': 'numeric_value',
                            'value': '10000',
                            'operator': 'greater_than_or_equal_to'
                        }
                    ],
                    'sub_conditions': []
                }
            }
        ]
    })
