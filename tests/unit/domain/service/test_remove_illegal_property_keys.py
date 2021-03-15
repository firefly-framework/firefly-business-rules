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

from firefly_business_rules.application import Container
import pytest

from firefly_business_rules.domain import RemoveIllegalPropertyKeys


def test_remove_illegal_property_keys(sut):
    data = {
        'valid_key': 'good',
        '_valid_key': 'good',
        'has-dashes': 'bad',
        '5_number_start': 'bad',
        '5-with-dashes': 'bad',
    }

    removed = sut(data)
    assert 'valid_key' in data
    assert '_valid_key' in data
    assert 'has-dashes' not in data
    assert '5_number_start' not in data
    assert '5-with-dashes' not in data
    assert 'has-dashes' in removed
    assert '5_number_start' in removed
    assert '5-with-dashes' in removed


@pytest.fixture()
def sut():
    return Container().mock(RemoveIllegalPropertyKeys)
