# -*- coding: utf-8 -*-

# This file is part of Workout Manager.
#
# Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from wger.core.models import License
from wger.settings_global import WGER_SETTINGS as settings
import fitbit
'''
Abstract model classes
'''


class AbstractLicenseModel(models.Model):
    '''
    Abstract class that adds license information to a model
    '''

    class Meta:
        abstract = True

    license = models.ForeignKey(License, verbose_name=_('License'), default=2)
    '''The item's license'''

    license_author = models.CharField(
        verbose_name=_('Author'),
        max_length=50,
        blank=True,
        null=True,
        help_text=_('If you are not the author, enter the name or '
                    'source here. This is needed for some licenses '
                    'e.g. the CC-BY-SA.'))
    '''The author if it is not the uploader'''


class AbstractSubmissionModel(models.Model):
    '''
    Abstract class used for model for user submitted data.

    These models have to be approved first by an administrator before they are
    shows in the website. There is also a manager that can be used:
    utils.managers.SubmissionManager
    '''

    class Meta:
        abstract = True

    STATUS_PENDING = '1'
    STATUS_ACCEPTED = '2'
    STATUS_DECLINED = '3'

    STATUS = (
        (STATUS_PENDING, _('Pending')),
        (STATUS_ACCEPTED, _('Accepted')),
        (STATUS_DECLINED, _('Declined')), )

    status = models.CharField(
        max_length=2, choices=STATUS, default=STATUS_PENDING, editable=False)
    '''Status of the submission, e.g. accepted or declined'''

class FitbitUser(models.Model):
    user = models.ForeignKey(User,verbose_name = _('User'),
    editable = False,on_delete=models.CASCADE)
    fitbit_id = models.CharField(max_length = 10)
    access_token =  models.CharField(max_length = 100)
    refresh_token = models.CharField(max_length = 100)
    
    def authenticate(self,user):
        key, secret = settings['FITBIT_CLIENT_ID'], settings['FITBIT_CLIENT_SECRET']
        auth = fitbit.FitbitOauth2Client(key, secret)
        self.user = user
        return auth.authorize_token_url()
       
    def completeAuth(self,user, code):
        key, secret = settings['FITBIT_CLIENT_ID'], settings['FITBIT_CLIENT_SECRET']
        auth = fitbit.FitbitOauth2Client(key, secret)
        data = auth.fetch_access_token(code)
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.fitbit_id = data['user_id']
        self.save()
        self.fitbit = fitbit.Fitbit(key, secret,
                                    access_token = self.access_token,
                                    refresh_token = self.refresh_token)
        return self

    def getWeightInfo(self,start = None,end = None):
        body_weight = self.fitbit.get_bodyweight()
        clean_data = [{'date':data['date'],'weight':data['weight']} for data in body_weight['weight']]
        return clean_data

