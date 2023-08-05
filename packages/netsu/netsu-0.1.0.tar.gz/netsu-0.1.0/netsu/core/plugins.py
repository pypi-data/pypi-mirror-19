# Copyright (C) 2016 Petr Horacek <phoracek@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pkg_resources


def get_definitions_updates():
    return _get_sorted_entry_points('netsu.plugins.definitions_updates')


def get_config_updates():
    return _get_sorted_entry_points('netsu.plugins.config_updates')


def get_state_updates():
    return _get_sorted_entry_points('netsu.plugins.state_updates')


def get_setup_steps():
    return _get_sorted_entry_points('netsu.plugins.setup_steps')


def get_force_cleanup_steps():
    return _get_sorted_entry_points('netsu.plugins.force_cleanup_steps')


def _get_sorted_entry_points(group):
    entry_points = list(pkg_resources.iter_entry_points(group=group))
    entry_points.sort(key=lambda entry_point: entry_point.name)
    return [entry_point.load() for entry_point in entry_points]
