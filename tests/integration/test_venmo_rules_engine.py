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

import firefly_business_rules.domain as domain
import firefly_business_rules.infrastructure as infra
import pytest

triggered = False


def test_convert_rule_set(engine: infra.VenmoRulesEngine, rule_set, transport):
    global triggered
    triggered = False

    def trigger(x):
        global triggered
        triggered = True

    transport.register_handler('accounting.RecordNewSale', trigger)
    engine.evaluate_rule_set(rule_set, {
        'id': 'abc123',
        'sales_code': 1,
        'price': 99.99,
        'on_sale': False,
    })

    assert triggered is True


@pytest.fixture()
def engine(container):
    return container.build(infra.VenmoRulesEngine)


@pytest.fixture()
def rule_set():
    return domain.RuleSet(
        name='Test Rules',
        input=domain.Input(
            name='sales.WidgetUpdated',
            variables=[
                domain.Variable(name='id', type='string'),
                domain.Variable(name='sales_code', type='number'),
                domain.Variable(name='price', type='number'),
                domain.Variable(name='on_sale', type='boolean'),
            ]
        ),
        conditions=domain.ConditionSet(
            all=True,
            conditions=[
                domain.Condition(name='id', operator='equal_to', value='abc123')
            ]
        ),
        commands=[
            domain.Command(context='accounting', name='RecordNewSale'),
        ]
    )
