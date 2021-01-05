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

from typing import List, Union

import firefly as ff


class Condition(ff.ValueObject):
    name: str = ff.required()
    operator: str = ff.required(validators=ff.IsOneOf((
        'equal_to', 'equal_to_case_insensitive', 'starts_with', 'ends_with', 'contains', 'matches_regex', 'non_empty',
        'greater_than', 'greater_than_or_equal_to', 'less_than', 'less_than_or_equal_to', 'is_true', 'is_false',
        'does_not_contain', 'contains_all', 'is_contained_by', 'shares_at_least_one_element_with',
        'shares_exactly_one_element_with', 'shares_no_elements_with'
    )))
    value: str = ff.required()


class Command(ff.ValueObject):
    id: str = ff.id_()
    name: str = ff.required(index=True)
    params: dict = ff.dict_()


class ConditionSet(ff.ValueObject):
    all: bool = ff.optional(default=True)
    conditions: List[Condition] = ff.list_()
    sub_conditions: List[ConditionSet] = ff.list_()


class Rule(ff.ValueObject):
    conditions: ConditionSet = ff.required()
    commands: List[Command] = ff.list_()


@ff.rest.crud()
class RuleSet(ff.AggregateRoot):
    id: str = ff.id_()
    name: str = ff.optional(index=True)
    rules: List[Rule] = ff.required()
