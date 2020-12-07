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
import json
from pprint import pprint

import firefly_business_rules.domain as domain
import firefly_business_rules.infrastructure as infra
import pytest

triggered = {}


def trigger(x):
    global triggered

    triggered[x] = False

    def inner(y):
        global triggered
        triggered[y] = True

    return lambda z: inner(x)


def test_convert_rule_set(engine: infra.VenmoRulesEngine, rule_set, transport):
    transport.register_handler('accounting.RecordNewSale', trigger('a'))
    engine.evaluate_rule_set(rule_set, {
        'id': 'abc123',
        'sales_code': 1,
        'price': 99.99,
        'on_sale': False,
    })

    assert triggered['a'] is True


async def test_api(client, transport, registry):
    transport.register_handler('accounting.RecordNewSale', trigger('a'))

    await client.post('/firefly-business-rules/rule-sets', data=json.dumps({
        'name': 'My Test Rule Set',
        'conditions': [{
            'all': True,
            'conditions': [
                {'name': 'id', 'operator': 'equal_to', 'value': 'abc123'},
            ],
            'commands': [{'context': 'accounting', 'name': 'RecordNewSale'}]
        }],
        'scopes': ['firefly_business_rules.RuleSet.write'],
    }))

    await client.post('/firefly-business-rules/evaluate-rules', data=json.dumps({
        'name': 'My Test Rule Set',
        'data': {
            'id': 'abc123',
            'sales_code': 1,
            'price': 99.99,
            'on_sale': False,
        }
    }))

    assert triggered['a'] is True


@pytest.fixture()
def engine(container):
    return container.build(infra.VenmoRulesEngine)


@pytest.fixture()
def rule_set():
    return domain.RuleSet(
        name='Test Rules',
        conditions=[
            domain.ConditionSet(
                all=True,
                conditions=[
                    domain.Condition(name='id', operator='equal_to', value='abc123')
                ],
                commands=[
                    domain.Command(context='accounting', name='RecordNewSale'),
                ]
            )
        ],
    )
