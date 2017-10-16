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
    
    def authenticate(self, user):
        self.user = user
        self.key, self.secret = settings['FITBIT_CLIENT_ID'], settings['FITBIT_CLIENT_SECRET']
        is_auth = self.isAuthenticated()
        print(is_auth)
        if is_auth:
            self.access_token = is_auth.access_token
            self.refresh_token = is_auth.refresh_token
            self.authenticated = True
            return self.authenticated
        
        return False

    def getUrl(self):
        auth = fitbit.FitbitOauth2Client(self.key, self.secret)
        return auth.authorize_token_url()

    def isAuthenticated(self):
        is_auth = FitbitUser.objects.filter(user=self.user).first()
        return is_auth
       
    def completeAuth(self, code):
        auth = fitbit.FitbitOauth2Client(self.key, self.secret)
        data = auth.fetch_access_token(code)
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.fitbit_id = data['user_id']
        self.authenticated = True
        self.save()
        return self

    def initFitbit(self):
        fitbit_instance = fitbit.Fitbit(self.key, self.secret,
                               access_token=self.access_token,
                               refresh_token=self.refresh_token)
        return fitbit_instance

    def getWeightInfo(self,start = None,end = None):
        fitbit_instance = self.initFitbit()
        body_weight = fitbit_instance.get_bodyweight()
        clean_data = [{'date':data['date'],'weight':data['weight']} for data in body_weight['weight']]
        return clean_data

