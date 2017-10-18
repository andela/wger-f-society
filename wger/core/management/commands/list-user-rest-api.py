# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from django.core.management.base import BaseCommand, CommandError
from tabulate import tabulate
from django.contrib.auth.models import User

from wger.core.models import UserProfile


class Command(BaseCommand):
    '''
    Management command to list users created via API
    '''
    help = 'List users'

    def add_arguments(self, parser):
        parser.add_argument('creators_username', type=str)

    def handle(self, **options):
        # check if creator exist
        creators_username = options['creators_username']
        User_creator = User.objects.filter(username=creators_username)
        if User_creator:
            all_users = UserProfile.objects.all().filter(created_by=creators_username)
            headers = ['USERNAME', 'EMAIL']
            table = []
            for user in all_users:
                table.append([user.user.username, user.user.email])
            self.stdout.write(tabulate(table, headers, tablefmt="rst"))
        else:
            raise CommandError('Creator do not exist')
