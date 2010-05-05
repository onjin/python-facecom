"""Python module for face.com API"""

import urllib
import urllib2
import json
import pprint

API_SERVER = 'http://api.face.com/'
API_DEBUG = False



class FaceRestClient(object):

    def __init__(self, api_key, api_secret, password = None, format = 'json'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.password = password
        self.format = format

        self.user_auth = {}

    def set_facebook_user(self, facebook_user, facebook_session):
        self.user_auth['fb_user'] = facebook_user
        self.user_auth['fb_session'] = facebook_session

    def set_twitter_user(self, twitter_user_name, twitter_password):
        self.user_auth['twitter_username'] = twitter_username
        self.user_auth['twitter_password'] = twitter_password

    def set_twitter_oauth_user(self, twitter_oauth_user, twitter_oauth_token, twitter_oauth_secret):
        self.user_auth['twitter_oauth_user'] = twitter_oauth_user
        self.user_auth['twitter_oauth_token'] = twitter_oauth_token
        self.user_auth['twitter_oauth_secret'] = twitter_oauth_secret

    def account_authenticate(self):
        return self.call_method('account/authenticate')

    def account_limits(self):
        return self.call_method('account/limits')

    def account_users(self, namespaces = None):
        return self.call_method('account/users', { 'namespaces': namespaces })


    def faces_detect(self, urls = None, filename = None, owner_ids = None, callback_url = None):
        params = {
            'urls': urls,
            'owner_ids': owner_ids,
            'callback_url': callback_url,
        }

        if filename:
            params['_file'] = '@' + filename,

        return self.call_method('faces/detect', params)

    def faces_recognize(self, urls = None, uids = None, namespace = None, train = None, filename = None, owner_ids = None, callback_url = None):
        params = {
            'urls': urls,
            'uids': uids,
            'namespace': namespace,
            'train': train,
            'owner_ids': owner_ids,
            'callback_url': callback_url,
            }

        if filename:
            params['_file'] = '@' + filename,

        return self.call_method('faces/recognize', params)

    def faces_train(self, uids, namespace = None, callback_url = None):
        return self.call_method('faces/train',
            {
                'uids': uids,
                'namespace': namespace,
                'callback_url': callback_url,
            })

    def faces_status(self, uids, namespace):
        return self.call_method('faces/status',
            {
                'uids': uids,
                'namespace': namespace,
            })

    def tags_add(self, url, x, y, width, height, label, uid = None, pid = None, tagger_id = None, owner_id = None):
        return self.call_method('tags/add',
            {
                'url': url,
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'label': label,
                'uid': uid,
                'pid': pid,
                'tagger_id': tagger_id,
                'owner_id': owner_id,
            })

    def tags_save(self, tids, uid = None, label = None, tagger_id = None):
        return self.call_method('tags/save',
            {
                'tids': tids,
                'label': label,
                'uid': uid,
                'tagger_id': tagger_id,
            })

    def tags_remove(self, tids, tagger_id = None):
        return self.call_method('tags/remove',
            {
                'tids': tids,
                'tagger_id': tagger_id,
            })

    def tags_get(self, urls = None, pids = None, filename = None, owner_ids = None, uids = None, namespace = None, filter = None, limit = None, together = None, order = None):
        params = {
            'urls': urls,
            'pids': pids,
            'owner_ids': owner_ids,
            'uids': uids,
            'together': together,
            'filter': filter,
            'order': order,
            'limit': limit,
            'namespace': namespace,
        }

        if filename:
            params['_file'] = '@' + filename,

        return self.call_url('tags/get', params)

    def facebook_get(self, uids, filter, limit, together, order):
        return self.call_method('facebook/get',
            {
                'uids': uids,
                'limit': limit,
                'together': together,
                'filter': filter,
                'order': order,
            })

    def call_method(self, method, params = {}):
        for key in params.keys():
            if not params[key]:
                del params[key]

        auth_params = {}

        if self.api_key:
            auth_params['api_key'] = self.api_key
        if self.api_secret:
            auth_params['api_secret'] = self.api_secret
        if self.password:
            auth_params['password'] = self.password

        if self.user_auth:
            auth_params['user_auth'] = ",".join(["%s:%s" % (x, self.user_auth[x]) for x in self.user_auth]) 


        params = auth_params.update( params)

        params = urllib.urlencode(auth_params)

        print "method:", method
        print "parms:", params

        request = urllib2.Request("%s/%s.%s" % (API_SERVER, method, self.format), params)

        response = urllib2.urlopen(request)
        return json.load(response)

