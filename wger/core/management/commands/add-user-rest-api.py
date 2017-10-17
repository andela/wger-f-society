# -*- coding: utf-8 *-*

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

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password

from wger.core.models import UserProfile


class Command(BaseCommand):
    '''
    A command that lets user registration
    '''

    help = 'Create users using a command'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('creators_username', type=str)
        parser.add_argument('creators_password', type=str)

    def handle(self, **options):
        # assert the creator exists
        creators_username = options['creators_username']
        creators_password = options['creators_password']
        User_creator = User.objects.get(username=creators_username)
        creators_profile = UserProfile.objects.get(user=User_creator)
        if User_creator and check_password(creators_password, creators_profile.user.password):
            # check username is already taken
            User_api = User.objects.filter(username=options['username'])
            if not User_api:
                new_api_user = User.objects.create_user(
                    username=options['username'],
                    email=options['email'],
                    password=options['password']
                )
                try:
                    new_api_user.save()
                    new_api_user_profile = UserProfile.objects.get(user=new_api_user)
                    new_api_user_profile.created_by = creators_profile
                    new_api_user_profile.save()
                    self.stdout.write("New app user created successfully")
                except IntegrityError as error:
                    raise CommandError('An error occured : ', error)
            else:
                raise CommandError('Username already taken')
        else:
            raise CommandError('Creator do not exist or the password is wrong')
