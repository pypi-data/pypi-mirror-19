"""Tests for OAuth2Reddit class."""

from __future__ import print_function, unicode_literals

from praw import Reddit, errors, decorators
from praw.objects import Submission
from six import text_type
from .helper import (PRAWTest, NewOAuthPRAWTest, USER_AGENT, betamax,
                     betamax_custom_header, mock_sys_stream)


class OAuth2RedditTest(PRAWTest):
    def setUp(self):
        self.configure()
        self.r = Reddit(USER_AGENT, site_name='reddit_oauth_test',
                        disable_update_check=True)

    def test_authorize_url(self):
        self.r.set_oauth_app_info(None, None, None)
        self.assertRaises(errors.OAuthAppRequired, self.r.get_authorize_url,
                          'dummy_state')
        self.r.set_oauth_app_info(self.r.config.client_id,
                                  self.r.config.client_secret,
                                  self.r.config.redirect_uri)
        url, params = self.r.get_authorize_url('...').split('?', 1)
        self.assertTrue('api/v1/authorize/' in url)
        params = dict(x.split('=', 1) for x in params.split('&'))
        expected = {'client_id': self.r.config.client_id,
                    'duration': 'temporary',
                    'redirect_uri': ('https%3A%2F%2F127.0.0.1%3A65010%2F'
                                     'authorize_callback'),
                    'response_type': 'code', 'scope': 'identity',
                    'state': '...'}
        self.assertEqual(expected, params)

    @betamax()
    @mock_sys_stream("stdin")
    def test_empty_captcha_file(self):
        # Use the alternate account because it has low karma,
        # so we can test the captcha.
        self.r.refresh_access_information(self.other_refresh_token['submit'])
        self.assertRaises(errors.InvalidCaptcha, self.r.submit,
                          self.sr, 'captcha test will fail', 'body')

    @betamax()
    def test_get_access_information(self):
        # If this test fails, the following URL will need to be visted in order
        # to obtain a new code to pass to `get_access_information`:
        # self.r.get_authorize_url('...')
        token = self.r.get_access_information('MQALrr1di8GzcnT8szbTWhLcBUQ')
        expected = {'access_token': self.r.access_token,
                    'refresh_token': None,
                    'scope': set(('identity',))}
        self.assertEqual(expected, token)
        self.assertEqual('PyAPITestUser2', text_type(self.r.user))

    @betamax()
    def test_get_access_information_with_invalid_code(self):
        self.assertRaises(errors.OAuthInvalidGrant,
                          self.r.get_access_information, 'invalid_code')

    @betamax()
    @mock_sys_stream("stdin")
    def test_inject_captcha_into_kwargs_and_raise(self):
        # Use the alternate account because it has low karma,
        # so we can test the captcha.
        self.r.refresh_access_information(self.other_refresh_token['submit'])

        # praw doesn't currently add the captcha into kwargs so lets
        # write a function in which it would and alias it to Reddit.submit
        @decorators.restrict_access(scope='submit')
        @decorators.require_captcha
        def submit_alias(r, sr, title, text, **kw):
            return self.r.submit.__wrapped__.__wrapped__(
                r, sr, title, text, captcha=kw.get('captcha')
            )
        self.assertRaises(errors.InvalidCaptcha, submit_alias, self.r,
                          self.sr, 'captcha test will fail', 'body')

    def test_invalid_app_access_token(self):
        self.r.clear_authentication()
        self.r.set_oauth_app_info(None, None, None)
        self.assertRaises(errors.OAuthAppRequired,
                          self.r.get_access_information, 'dummy_code')

    def test_invalid_app_authorize_url(self):
        self.r.clear_authentication()
        self.r.set_oauth_app_info(None, None, None)
        self.assertRaises(errors.OAuthAppRequired,
                          self.r.get_authorize_url, 'dummy_state')

    @betamax()
    def test_invalid_set_access_credentials(self):
        self.assertRaises(errors.OAuthInvalidToken,
                          self.r.set_access_credentials,
                          set(('identity',)), 'dummy_access_token')

    def test_oauth_scope_required(self):
        self.r.set_oauth_app_info('dummy_client', 'dummy_secret', 'dummy_url')
        self.r.set_access_credentials(set('dummy_scope',), 'dummy_token')
        self.assertRaises(errors.OAuthScopeRequired, self.r.get_me)

    def test_raise_client_exception(self):
        def raise_client_exception(*args):
            raise errors.ClientException(*args)

        self.assertRaises(errors.ClientException, raise_client_exception)
        self.assertRaises(errors.ClientException, raise_client_exception,
                          'test')

        ce_message = errors.ClientException('Test')
        ce_no_message = errors.ClientException()
        self.assertEqual(ce_message.message, str(ce_message))
        self.assertEqual(ce_no_message.message, str(ce_no_message))

    def test_raise_http_exception(self):
        def raise_http_exception():
            raise errors.HTTPException('fakeraw')

        self.assertRaises(errors.HTTPException, raise_http_exception)
        http_exception = errors.HTTPException('fakeraw')
        self.assertEqual(http_exception.message, str(http_exception))

    def test_raise_oauth_exception(self):
        oerrormessage = "fakemessage"
        oerrorurl = "http://oauth.reddit.com/"

        def raise_oauth_exception():
            raise errors.OAuthException(oerrormessage, oerrorurl)

        self.assertRaises(errors.OAuthException, raise_oauth_exception)
        oauth_exception = errors.OAuthException(oerrormessage, oerrorurl)
        self.assertEqual(oauth_exception.message +
                         " on url {0}".format(oauth_exception.url),
                         str(oauth_exception))

    def test_raise_redirect_exception(self):
        apiurl = "http://api.reddit.com/"
        oauthurl = "http://oauth.reddit.com/"

        def raise_redirect_exception():
            raise errors.RedirectException(apiurl, oauthurl)

        self.assertRaises(errors.RedirectException, raise_redirect_exception)
        redirect_exception = errors.RedirectException(apiurl, oauthurl)
        self.assertEqual(redirect_exception.message, str(redirect_exception))

    @betamax()
    def test_scope_history(self):
        self.r.refresh_access_information(self.refresh_token['history'])
        self.assertTrue(list(self.r.get_redditor(self.un).get_upvoted()))

    @betamax()
    def test_scope_identity(self):
        self.r.refresh_access_information(self.refresh_token['identity'])
        self.assertEqual(self.un, self.r.get_me().name)

    @betamax()
    def test_scope_mysubreddits(self):
        self.r.refresh_access_information(self.refresh_token['mysubreddits'])
        self.assertTrue(list(self.r.get_my_moderation()))

    @betamax()
    def test_scope_creddits(self):
        # Assume there are insufficient creddits.
        self.r.refresh_access_information(
            self.refresh_token['creddits'])
        redditor = self.r.get_redditor('bboe')
        sub = self.r.get_submission(url=self.comment_url)

        # Test error conditions
        self.assertRaises(TypeError, sub.gild, months=1)
        for value in (False, 0, -1, '0', '-1', 37, '37'):
            self.assertRaises(TypeError, redditor.gild, value)

        # Test object gilding
        self.assertRaises(errors.InsufficientCreddits, redditor.gild)
        self.assertRaises(errors.InsufficientCreddits, sub.gild)
        self.assertRaises(errors.InsufficientCreddits, sub.comments[0].gild)

    @betamax()
    def test_scope_privatemessages(self):
        self.r.refresh_access_information(
            self.refresh_token['privatemessages'])
        self.assertTrue(list(self.r.get_inbox()))

    @betamax()
    def test_scope_read(self):
        self.r.refresh_access_information(self.refresh_token['read'])
        self.assertTrue(self.r.get_subreddit(self.priv_sr).subscribers > 0)
        fullname = '{0}_{1}'.format(self.r.config.by_object[Submission],
                                    self.priv_submission_id)
        method1 = self.r.get_info(thing_id=fullname)
        method2 = self.r.get_submission(submission_id=self.priv_submission_id)
        self.assertEqual(method1, method2)

    @betamax()
    def test_scope_read_get_front_page(self):
        self.r.refresh_access_information(self.refresh_token['mysubreddits'])
        subscribed = list(self.r.get_my_subreddits(limit=None))
        self.r.refresh_access_information(self.refresh_token['read'])
        for post in self.r.get_front_page():
            self.assertTrue(post.subreddit in subscribed)

    @betamax()
    def test_set_access_credentials(self):
        self.assertTrue(self.r.user is None)
        result = self.r.refresh_access_information(
            self.refresh_token['identity'], update_session=False)
        self.assertTrue(self.r.user is None)
        self.r.set_access_credentials(**result)
        self.assertFalse(self.r.user is None)

    @betamax()
    def test_set_access_credentials_with_list(self):
        self.assertTrue(self.r.user is None)
        result = self.r.refresh_access_information(
            self.refresh_token['identity'], update_session=False)
        self.assertTrue(self.r.user is None)
        result['scope'] = list(result['scope'])
        self.r.set_access_credentials(**result)
        self.assertFalse(self.r.user is None)

    @betamax()
    def test_set_access_credentials_with_string(self):
        self.assertTrue(self.r.user is None)
        result = self.r.refresh_access_information(
            self.refresh_token['identity'], update_session=False)
        self.assertTrue(self.r.user is None)
        result['scope'] = ' '.join(result['scope'])
        self.r.set_access_credentials(**result)
        self.assertFalse(self.r.user is None)

    @betamax()
    @mock_sys_stream("stdin", "ljgtoo")
    def test_solve_captcha(self):
        # Use the alternate account because it has low karma,
        # so we can test the captcha.
        self.r.refresh_access_information(self.other_refresh_token['submit'])
        self.r.submit(self.sr, 'captcha test', 'body')

    @betamax()
    @mock_sys_stream("stdin", "DFIRSW")
    def test_solve_captcha_on_bound_subreddit(self):
        # Use the alternate account because it has low karma,
        # so we can test the captcha.
        self.r.refresh_access_information(self.other_refresh_token['submit'])
        subreddit = self.r.get_subreddit(self.sr)

        # praw doesn't currently have a function in which require_captcha
        # gets a reddit instance from a subreddit and uses it, so lets
        # write a function in which it would and alias it to Reddit.submit
        @decorators.restrict_access(scope='submit')
        @decorators.require_captcha
        def submit_alias(sr, title, text, **kw):
            return self.r.submit.__wrapped__.__wrapped__(
                self.r, sr, title, text, captcha=kw.get('captcha')
            )
        submit_alias(subreddit, 'captcha test on bound subreddit', 'body')

    @betamax()
    def test_oauth_without_identy_doesnt_set_user(self):
        self.assertTrue(self.r.user is None)
        self.r.refresh_access_information(self.refresh_token['edit'])
        self.assertTrue(self.r.user is None)


class AutoRefreshTest(NewOAuthPRAWTest):
    @betamax_custom_header()
    def test_auto_refresh_token(self):
        # this test wasn't cached before the new test was made
        # so the new app info needs to be set to avoid 401s
        # also, the redirect uri doesn't need to be set on refreshes,
        # but praw does this anyway. Changing this now would break
        # all prior tests. The redirect uri should be removed and
        # all tests rerecorded later.
        with self.set_custom_header_match('test_auto_refresh_token__initial'):
            self.r.refresh_access_information(
                self.refresh_token['auto_refresh'])
        old_token = self.r.access_token

        self.r.access_token += 'x'  # break the token
        with self.set_custom_header_match('test_auto_refresh_token__refresh'):
            # TODO: refreshing r.user wasn't actually updating the token
            # because of special oauth handling in _get_json_dict of
            # reddit content objects. Leaving this as a note until I
            # fix it in the future
            list(self.r.get_new(limit=5))
        current_token = self.r.access_token
        self.assertNotEqual(old_token, current_token)

        with self.set_custom_header_match('test_auto_refresh_token__after'):
            list(self.r.get_new(limit=5))
        self.assertEqual(current_token, self.r.access_token)
