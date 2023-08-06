#!/usr/bin/env python

# XXX FIX: no redirect after logout link used??

"""
Framework free Authentication Methods for CGI scripts

Includes the following classes:

        * `BasicAuth' which depends on web server "Basic" authentication
        * Cookie based classes `SessionCookieAuth' and `StatelessCookieAuth'
        * Hidden field based classes `SessionHiddenAuth' and
          `StatelessHiddenAuth'

The Cookie and Hidden classes use JavaScript/SHA1 hashing to avoid
sending passwords as clear text.

Class constructor must be called BEFORE HTTP headers are output.
All Authentication object constructors either return (possibly having
output cookie headers) or exit (having output a login form, or error
message).

cgiauth.py functions as a test if invoked as a CGI script, and as a
password file creator if invoked from the command line.

Developed/tested under Python 2.5
"""

# Copyright (C) 2009, 2010 by Philip L. Budne
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.

# TODO:
# add tests for Hidden....Auth classes
# add PWFile.set_password(user, password)?
# enable alert for "need user and password"?
# make demo logger prepend addr & user (pass "extra" arg)
# allow arbitrary page title/login banner (title param)
# work harder to prevent password auto-fill (use random name for pw field?)
# add set_user(); call check_logout?
# pass "salt" to login form in a variable (not a form field)?
# wrap login objects, and return an Auth object with less data stored in it?
# provide CGI admin screens: add user, delete user.
# provide CGI change password screen:
#       use old hashed password as key to en/decrypt new hashed password?
#               requires JavaScript symmetric encryption (ie; AES) function
#       RSA encrypt new password w/ supplied public key
#       export implications?

# have check_session return entire data object?
#
# WAY FUTURE?
# pickle environment (and stdin data) so
#       POST/GET on timed out session doesn't lose data
# allow per-user salt & hash method (use AJAX to fetch)?

# BUGS:
# if user is POSTing with an expired cookie, form data is lost
#       backing up two pages and submitting would restore it?!

__author__ = "Phil Budne <phil@ultimate.com>"
__revision__ = "$Id: cgiauth.py,v 1.35 2010/01/22 22:15:18 phil Exp $"
__version__ = "0.9.1"

import os
import sys
import time
import uuid             # session id & salt generation
import hmac
import Cookie
import hashlib
import pickle           # session data storage
import string           # Template (switch to 2.6+ str.format?)
import re

# application salt stored in password file as (first) user
# also identifies algorithm version used to hash user/pw/salt
#       cannot have per-user salt, or per-user algorithm,
#       since user isn't known when form is output
#       (without seperate form for user or AJAX)
SALTUSER = "-*-SALT1-*-"

# time before a login screen times out (in seconds)
LOGIN_WINDOW = 5*60

# default session time-to-live (in seconds)
DEFTTL = 15 * 60

class Auth(object):
    """CGI Authentication base class;  All Auth.... constructors
       MUST be called from CGI script *BEFORE* HTTP headers are output.
       All may::
       * Output a login form (and exit)
       * Output an error message and exit
       * Return after successful authentication, possibly having output
         an HTTP "Set-Cookie:" header

       The returned object is guaranteed to have a `user' attribute,
       and may provide `logout_url()' and/or `logout_button()' methods"""

    def __init__(self, logger):
        self.logger = logger
        self.addr = os.environ.get('REMOTE_ADDR', '-')
        
    def content_html(self):
        """method to output content-type: text/html header"""
        print "Content-Type: text/html"
        print ""

    def no_cache(self):
        """Try to get Internet Exploder not to cache CGI output!"""
        agent = os.environ.get('HTTP_USER_AGENT','')
        if agent.find("MSIE") != -1:
            self.debug("detected IE")
            # from moinmoin-1.5.5.a request.py:
            print "Pragma: no-cache"
            print "Cache-Control: no-cache"
            print "Expires: -1"

    def fatal_http(self, error):
        """administrator/config error"""
        self.content_html()
        print '''<html>
<head><title>%s</title></head>
<body><h1>%s</h1></body>
</html>''' % (error, error)
        self.fatal(error)

    # NOTE! let logger object prepend addr
    def debug(self, message):
        """log debug message"""
        if self.logger:
            self.logger.debug(message)

    def info(self, message):
        """log info message"""
        if self.logger:
            self.logger.info(message)

    def warning(self, message):
        """log warning message"""
        if self.logger:
            self.logger.warning(message)

    def error(self, message):
        """log error message"""
        if self.logger:
            self.logger.error(message)

    def fatal(self, message):
        """log error message"""
        if self.logger:
            self.logger.fatal(message)
        sys.exit(0)

class BasicAuth(Auth):
    """Auth method that depends on "basic authentication" done by web server
       Either succeeds immediately, or prints error and exits"""

    def __init__(self, name, logger):
        """exits if basic authentication not performed by web server"""
        Auth.__init__(self, logger)
        user = os.environ.get('REMOTE_USER')
        atype = os.environ.get('AUTH_TYPE')

        # allow Digest too???
        if not user or not self.addr or atype != 'Basic':
            # try kicking client.  THIS MAY BE POINTLESS!
            #
            # According to http://support.tigertech.net/php-http-auth
            # this .htaccess file will cause Apache to pass
            # AUTHORIZATION environment variable to CGI scripts, which
            # can be decoded to user:password with base64.decodestring():
            # RewriteEngine on
            # RewriteRule .* - [env=AUTHORIZATION:%{HTTP:Authorization},last]
            # other refs:
            # http://osdir.com/ml/python.webware/2005-04/msg00012.html
            # http://wiki.w4py.org/http-authentication.html
            # for more, search for: http:authorization rewriterule
            error = '401 Authorization Required'
            # look at, pass back SERVER_PROTOCOL; skip for HTTP/0.9?
            print 'HTTP/1.0 %s' % error
            print 'WWW-Authenticate: Basic realm="%s"' % name
            self.fatal_http(error)
            # NOTREACHED

        self.info(user)
        self.user = user

# login screen template; processed using string.Template (switch to
# 2.6+ str.format?)  used to initialize PWAuth.LOGIN_TEMPLATE
# (which can be overridden)

_LOGIN_TEMPLATE = '''
<html>
<head>
    <title>${TITLE}</title>
    ${EXTRA_HEAD}
</head>
<body>
${EXTRA_BODY_TOP}
<!-- login form by http://pypi.python.org/pypi/cgiauth/ -->
<noscript>
<div class="msg">This page requires JavaScript</div>
</noscript>
<script>
if (navigator.cookieEnabled) {
    document.write('${LOGIN_FORM}');
    // no bound methods in JavaScript...
    window.onload = function() { document.login.user.focus(); }
}
else
    document.write('<div class="msg">This page requires cookies for login</div>');
</script>
'''

# this is inserted into page via document.write (above) after newlines removal
_LOGIN_FORM = '''
<p align=center>
<div class="msg">${MSG}</div>
<form name="login" method="post" onsubmit="return submit_hook(this);"${AUTOC}>
    <table align=center>
    <tr><td class="head">${TITLE}
    <tr><td><table align="center" border=1>
            <tr><td><b>Username:</b>
                <td><input type="text" name="user" value="" size="30">
            <tr><td><b>Password:</b>
                <td><input type="password" name="password" value="" size="30${AUTOC}">
            ${EXTRA_ROWS}
            </table>
    <tr><td align=center><input type="submit" value="Login">
    </table>
    <input type="hidden" name="salt" value="${SALT}">
    <input type="hidden" name="nonce" value="${NONCE}">
    <input type="hidden" name="hashedpw">
    ${EXTRA_HIDDEN}
</form>
${EXTRA_BODY_TOP}
${FOOTER}
'''

class PWAuth(Auth):
    """Base class for authentication using SHA1 hashed passwords.

      Login screen uses JavaScript SHA1 HMAC to
      calculate hash of user, password and back-end provided values.

      User passwords are stored in non-reversable form
      (hash of user, password and application specific salt string)

      Passwords for test passed over the network are the above,
      hashed with the time the password screen was output
      (login screen is only valid for a limited time).
      """

    # name of magic field, which if set logs user out.
    LOGOUT_FIELD = 'logout'

    # default login screen template: may be overridden
    LOGIN_TEMPLATE = _LOGIN_TEMPLATE
    LOGIN_FORM = _LOGIN_FORM

    # extra items to add to LOGIN_TEMPLATE:
    AUTOCOMPLETE = ' autocomplete="off"'

    # extra head items (styling):
    EXTRA_HEAD = '''  <style type="text/css">
    .head {
        text-align: center; font-size: larger; font-weight: bold;
        background-color: aqua
    }
    .msg {
        text-align: center;
        font-size: larger; font-weight: bold; color: red
    }
  </style>'''

    # extra body items at top
    EXTRA_BODY_TOP = '<!-- EXTRA_BODY_TOP here -->'
    # extra body items after form
    EXTRA_BODY_BOT = '<!-- EXTRA_BODY_BOT here -->'
    # extra rows for login form table
    EXTRA_ROWS = '<!-- EXTRA_ROWS here -->'
    # extra hidden input items in form
    EXTRA_HIDDEN = '<!-- EXTRA_HIDDEN here -->'
    # login page footer:
    FOOTER = '''<p>&nbsp;<p>&nbsp;<p>&nbsp;
<font size="-1">login screen by
<a href="http://pypi.python.org/pypi/cgiauth/">cgiauth %s</a></font>''' % \
        __version__
    # Extra JavaScript code
    EXTRA_JAVASCRIPT_CODE = '// EXTRA_JAVASCRIPT_CODE here'

    def __init__(self, name, fields, pwfile, salt, ttl, logger, title):
        """`name' is application name, used for cookie, printed on login screen
           `fields' are CGI fields from `cgi.FieldStorage()'
           `pwfile' is PWFile object (or path to password file)
           `salt' is application specific salt string
                (if not supplied, will be fetched from password file)
           `ttl' is time-to-live for session (in seconds); zero means endless
           `logger' if supplied, is a logger object (ala `logging' module)
           `title' is optional title for login screen"""
        Auth.__init__(self, logger)

        # maintain backwards compatibility; accept string
        if isinstance(pwfile, basestring):
            pwfile = PWFile(pwfile)

        if not pwfile.exists():
            self.fatal_http("password file not found")
            # NOTREACHED
        # croak if pwfile is world read?

        if salt is None:
            salt = pwfile.get_hashed_password(SALTUSER)
            if not salt:
                self.fatal_http("needs salt!")

        self.name = name
        self.pwfile = pwfile
        self.salt = salt
        self.ttl = ttl
        if title is None:
            title = "%s login" % name
        self.title = title

    def check_logout(self, fields, user=""):
        """check if this is a logout request"""
        # '?logout=anything' as CGI params forces logout
        # (ie; fetch of "logout_url()", or click on "logout_button()"
        # value is ignored, as Python "cgi" package discards
        # keys without values (unless cgi.FieldStorage is called with
        # keep_blank_values=True)
        if self.LOGOUT_FIELD not in fields:
            return

        self.info("logout: %s" % user)
        self.remove_session()

        if os.environ.get('REQUEST_METHOD','') == 'POST':
            # only one round trip, gives "logged out" message
            # but leaves '?logout=...' in URL unless
            # got here via POST (ie; when logout_button() was used)
            self.login_form("logged out")
            # NOTREACHED

        # clears ?logout=... from url by redirecting
        # but requires another HTTP fetch and CGI invocation.
        # added PATH_INFO, but may still not be right!
        #
        # COULD have try having logout_url() return
        #   javascript:document.cgiauth_logout.submit()?!
        self.clear_authenticator()
        self.info("output redirect")
        print 'Location: %s%s\n' % (os.environ.get('SCRIPT_NAME'),
                                    os.environ.get('PATH_INFO',''))
        sys.exit(0)

    def remove_session(self, sid=None):
        """remove any session data stored on server"""
        pass

    def login_form(self, msg=""):
        """output password form and exit; LOGIN_TEMPLATE can be overridden"""

        def crunch(input_string, iscode):
            """crunch whitespace from JavaScript code and HTML.
               For putting login form into a document.write()
               and making SHA1 code smaller"""
            if iscode:
                # code: kill // comments (breaks URLs)
                input_string = re.sub(r"[\s]*//.*\n", "\n", input_string)
            return re.sub(r"\n[\s]*", " ", input_string)

        self.clear_authenticator()
        self.content_html()
        temp1 = string.Template(self.LOGIN_FORM)
        params = {'NAME': self.name,
                  'MSG': msg,
                  'SALT': self.salt,
                  'TITLE': self.title,
                  'NONCE': time.time(),
                  'AUTOC': self.AUTOCOMPLETE,
                  'EXTRA_BODY_TOP': self.EXTRA_BODY_TOP,
                  'EXTRA_BODY_BOT': self.EXTRA_BODY_BOT,
                  'EXTRA_ROWS': self.EXTRA_ROWS,
                  'EXTRA_HEAD': self.EXTRA_HEAD,
                  'EXTRA_HIDDEN': self.EXTRA_HIDDEN,
                  'FOOTER': self.FOOTER }
        login_form = crunch(temp1.substitute(params), False)
        params['LOGIN_FORM'] = login_form
        temp2 = string.Template(self.LOGIN_TEMPLATE)
        print temp2.substitute(params)
        print '<script>'
        print crunch(_JAVASCRIPT_CODE, True)
        print crunch(self.EXTRA_JAVASCRIPT_CODE, True)
        print '</script>'
        print '</body>'
        print '</html>'
        sys.exit(0)

    def logout_url(self):
        """returns URL to GET to log out"""
        # don't depend on FieldStorage called w/ keep_blank_values=True
        logout = '?%s=1' % self.LOGOUT_FIELD
        # try to deal with PATH_INFO by giving absolute path
        # may still not be right
        path_info = os.environ.get('PATH_INFO')
        if path_info:
            return os.environ.get('SCRIPT_NAME') + path_info + logout
        # return relative path
        return logout

    def logout_button(self):
        """return a form+button to logout (via POST); 
           allows logout without a redirect"""
        return ('<form method="POST" name="cgiauth_logout">' +
                '<input type="submit" name="%s" value="Logout">' +
                '</form>') % self.LOGOUT_FIELD

    def check_login_logout(self, fields):
        """returns 3-tuple: (user, nonce, hash(hashedpw, nonce))
           or outputs new login form (or redirect) and exits"""
        self.no_cache()
        self.check_logout(fields)
        return self._check_login_form(fields)

    def _check_login_form(self, fields):
        """returns 3-tuple: (user, nonce, hash(hashedpw, nonce))
           or outputs new login form and exits"""

        if 'user' in fields and 'nonce' in fields and 'hashedpw' in fields:
            # guard against replay (old nonce) or future value
            user = fields.getfirst('user')
            nonce = fields.getfirst('nonce')
            delta = time.time() - float(nonce)
            if delta < 0 or delta > LOGIN_WINDOW:
                self.warning("%s: timed out" % user)
                self.login_form("login timed out")
                # NOTREACHED

            resp = fields.getfirst('hashedpw')
            refpw = self.pwfile.get_hashed_password(user)
            if check_hashed_password(resp, nonce, refpw):
                self.info("%s: success" % user)
                return (user, nonce, resp)
            self.error("%s: bad password" % user)
            self.login_form('login failed')
            # NOTREACHED
        self.info("output form")
        self.login_form()
        # NOTREACHED

class CookieAuth(PWAuth):
    """base class for cookie-based Authentication schemes"""
    def __init__(self, name, fields, pwfile, salt, ttl, logger,
                 cookie_attrs, title):
        """`name' is application name, used for cookie, printed on login screen
           `fields' are CGI fields from `cgi.FieldStorage()'
           `pwfile' is PWFile object
           `salt' is application specific salt string
                (if not supplied, will be fetched from password file)
           `ttl' is time-to-live for session (in seconds); zero means endless
           `logger' if supplied, is a logger object (ala `logging' module)
           `cookie_attrs' is optional dictionary of cookie attributes
           `title' is optional title for login screen"""
        PWAuth.__init__(self, name, fields, pwfile, salt, ttl, logger, title)
        self.cookie_attrs = cookie_attrs
        self.authenticator = None

        # extract cookie, if any:
        cookie_string = os.environ.get('HTTP_COOKIE')
        if cookie_string:
            cookies = Cookie.SimpleCookie()
            cookies.load(cookie_string)
            if cookies.get(self.name):
                self.authenticator = cookies[self.name].value

    def set_authenticator(self, data):
        """output header to set cookie"""
        # for session cookies, so don't set `expires' or `max-age' keys
        cookies = Cookie.SimpleCookie()
        cookies[self.name] = data
        # Set the RFC 2109 required header.
        cookies[self.name]['version'] = 1
        # mix user supplied attributes into morsel
        if self.cookie_attrs:
            cookies[self.name].update(self.cookie_attrs)
        print str(cookies)

    def clear_authenticator(self):
        """output header to clear/delete existing cookie"""
        cookies = Cookie.SimpleCookie()
        cookies[self.name] = ''
        cookies[self.name]['expires'] = -1
        cookies[self.name]['max-age'] = 0
        print str(cookies)

class HiddenAuth(PWAuth):
    """base class for hidden field Authentication schemes"""
    def __init__(self, name, fields, pwfile, field_name, salt, ttl,
                 logger, title):
        """`name' is application name, used for cookie, printed on login screen
           `fields' are CGI fields from `cgi.FieldStorage()'
           `pwfile' is PWFile object
           `field_name' is name of hidden field w/ authenticator data
           `salt' is application specific salt string
                (if not supplied, will be fetched from password file)
           `ttl' is time-to-live for session (in seconds); zero means endless
           `logger' if supplied, is a logger object (ala `logging' module)
           `cookie_attrs' is optional dictionary of cookie attributes
           `title' is optional title for login screen"""
        PWAuth.__init__(self, name, fields, pwfile, salt, ttl, logger, title)
        self.authenticator = fields.getfirst(field_name)

    def set_authenticator(self, data):
        """save outgoing authenticator data"""
        self.authenticator = data

    def clear_authenticator(self):
        """clear authenticator"""
        self.authenticator = None

    def get_authenticator(self):
        """return authenticator data for hidden field in user form"""
        return self.authenticator

class SessionAuthMixin(Auth):
    """mixin for session-id based authentication.
       authenticator is a uuid, and must be looked
       up in a disk-based cache of sessions."""

    def __init__(self, name, fields, session_dir, ttl, extend):
        """`name' is application name, user for cookie, printed on login screen
           `fields' are CGI fields from `cgiFieldStorage()'
           `session_dir' is directory for session data storage
                (must be CGI writable)
           `ttl' is time-to-live for session (in seconds); zero means endless
           `extend' if non-zero, session will be extended if
                `extend' or less seconds left in session time to live"""
        if not os.path.isdir(session_dir):
            self.fatal_http("session directory does not exist")
            # NOTREACHED

        sstat = os.stat(session_dir)
        if (sstat.st_mode & 07):
            self.fatal_http("session directory error")
            # NOTREACHED

        self.session_dir = session_dir
        now = int(time.time())
        if self.authenticator:
            sid = self.authenticator
            # check for good session even if logging out, to show user
            user = self.check_session(sid, name, now, ttl, extend)
            self.check_logout(fields, user)
            if user:
                # avoid logging session id
                self.info("%s: good session" % user)
                self.user = user
                return

        # validate form input, or output new form and exit
        user, _, _ = self.check_login_logout(fields)

        # here on sucessful (re)login
        sid = self.store_session(user, name, now)
        # avoid logging session id

        # output header to set cookie
        self.set_authenticator(sid)
        self.user = user

    def remove_session(self, sid=None):
        """remove server session data file"""
        if not sid and self.authenticator:
            sid = self.authenticator
        if not sid or not self.valid_sid(sid):
            return

        path = os.path.join(self.session_dir, sid)
        if os.path.isfile(path):
            os.unlink(path)

    def generate_sid(self):
        """generate a unique session id.  must be a large/sparse space!"""
        return str(uuid.uuid4())

    def valid_sid(self, sid):
        """validate a session id;
           session id used in filename, make sure no monkey biz!!"""
        return sid.replace('-','').isalnum()

    def fetch(self, sid):
        """fetch session data; override to replace storage method"""
        path = os.path.join(self.session_dir, sid)
        if not os.path.isfile(path):
            return None

        # check for (and remove?) ancient files?

        try:
            # use "with"?
            rfd = file(path)
            data = pickle.load(rfd)
            rfd.close()
        except Exception:
            return None

        return data

    def store(self, sid, data):
        """store session data; override to replace storage method"""
        path = os.path.join(self.session_dir, sid)
        wfd = open(path, 'w')
        pickle.dump(data, wfd)
        wfd.close()

    def check_session(self, sid, name, now, ttl, extend):
        """check if session id `sid' is valid; return user or None"""
        if not self.valid_sid(sid):
            self.warning("invalid session id '%s'" % sid)
            return None

        data = self.fetch(sid)
        if not data:
            self.warning("non-existant session '%s'" % sid)
            return None

        user = data.get('user')
        if not user:
            self.warning("no user for session '%s'" % sid)
            self.remove_session(sid) # remove bad file
            return None

        # not for this application (stolen sid)??
        if data.get('name') != name:
            self.warning("wrong app name '%s'" % name)
            return None

        if 'expires' in data:
            # check if expired
            session_ttl = data['expires'] - now
            if session_ttl < 0:
                self.remove_session(sid)
                self.info("expired session '%s'" % sid)
                self.login_form("session expired")
                # NOTREACHED

            # extend session if <= `extend' seconds left in ttl
            if extend and ttl and session_ttl <= extend:
                self.info("extended session '%s'" % sid)
                data['expires'] = now + ttl
                data['addr'] = self.addr
                self.store(sid, data)
        return user

    def store_session(self, user, name, now):
        """store new session; returns new session id"""
        sid = self.generate_sid()
        data = { 'user': user,
                 'name': name,
                 'login' : now,
                 'addr': self.addr }
        if self.ttl > 0:
            data['expires'] = now + self.ttl

        self.store(sid, data)
        return sid

class StatelessAuthMixin(Auth):
    """Stateless authentication mixin.
       Authenticator contains: user/time/hash(hashedpw,time);
       Does not depend on server state data,
       BUT exposes user names (unless encyption methods overridden),
       Requires password file lookup on each authentication."""
    SEP = '|'

    def __init__(self, name, fields, pwfile, ttl, extend):
        """`name' is application name, user for cookie, printed on login screen
           `fields' are CGI fields from `cgi.FieldStorage()'
           `pwfile' is PWFile object, must be CGI readable
           `ttl' is time-to-live for session (in seconds); zero means endless
           `extend' if non-zero, session will be extended if
                `extend' or less seconds left in session time to live"""

        if self.authenticator:
            auth_value = self.decrypt(self.authenticator)
            items = auth_value.split(self.SEP)
            if len(items) == 3:
                resp, when, user = items
                self.check_logout(fields, user)
                now = time.time()
                elapsed = now - float(when)
                if elapsed > 0 and (ttl == 0 or elapsed < ttl):
                    refpw = self.pwfile.get_hashed_password(user)
                    if check_hashed_password(resp, when, refpw):
                        if ttl and extend and ttl-elapsed <= extend:
                            # NOTE! `now' should be floating point time()!!
                            hashedpwn = hashpwn(refpw, now)
                            self.set_authenticator(
                                 self.make_authenticator(
                                      hashedpwn, now, user))
                            self.info("%s: extended" % user)
                        else:
                            self.info("%s: good authenticator" % user)
                        self.user = user
                        return
                else:
                    self.warning("%s: session expired" % user)
                    self.login_form("session expired")
                    # NOTREACHED
            # clear cookie:
            self.clear_authenticator()

        # validate login form, or output new one
        user, nonce, hashedpwn = self.check_login_logout(fields)

        # here on successful login, make cookie and set it
        self.set_authenticator(self.make_authenticator(hashedpwn, nonce, user))
        self.user = user

    def make_authenticator(self, hashedpwn, nonce, user):
        """return cookie data"""
        return self.encrypt(self.SEP.join([hashedpwn, str(nonce), user]))

    def encrypt(self, plaintext):
        """override this method to provide an encryption algorithm to avoid
           sending cookie (contains username) in the clear; must return
           a printable (cookie safe) representation"""
        return plaintext

    def decrypt(self, encrypted):
        """override this method to decode and decrypt a cookie"""
        return encrypted

class SessionCookieAuth(SessionAuthMixin, CookieAuth):
    """cookie based authentication using session cookie.
       session cookie is a uuid, and must be looked
       up in a disk-based cache of sessions."""

    def __init__(self, name, fields, pwfile, session_dir,
                 salt=None, ttl=DEFTTL, logger=None, extend=0,
                 cookie_attrs=None, title=None):
        """`name' is application name, user for cookie, printed on login screen
           `fields' are CGI fields from `cgiFieldStorage()'
           `pwfile' is PWFile object, must be CGI readable
           `session_dir' is directory for session data storage
                (must be CGI writable)
           `salt' is application specific salt string
                (if not supplied, will be fetched from password file)
           `ttl' is time-to-live for session (in seconds); zero means endless
           `logger' if supplied, is a logger object (ala `logging' module)
           `extend' if non-zero, session will be extended if
                `extend' or less seconds left in session time to live
           `cookie_attrs' is optional dictionary of cookie attributes
           `title' is optional title for login screen"""
        CookieAuth.__init__(self, name, fields, pwfile, salt,
                            ttl, logger, cookie_attrs, title)
        SessionAuthMixin.__init__(self, name, fields, session_dir, ttl, extend)

class StatelessCookieAuth(StatelessAuthMixin, CookieAuth):
    """Stateless cookie based authentication;
       Cookie contains: user/time/hash(hashedpw,time);
       Does not depend on server state data,
       BUT exposes user names (unless encyption methods overridden),
       Requires password file lookup on each authentication."""
    def __init__(self, name, fields, pwfile,
                 salt=None, ttl=DEFTTL, logger=None, cookie_attrs=None,
                 extend=0, title=None):
        """`name' is application name, user for cookie, printed on login screen
           `fields' are CGI fields from `cgi.FieldStorage()'
           `pwfile' is PWFile object, must be CGI readable
           `salt' is application specific salt string
                (if not supplied, will be fetched from password file)
           `ttl' is time-to-live for session (in seconds); zero means endless
           `logger' if supplied, is a logger object (ala `logging' module)
           `cookie_attrs' is optional dictionary of cookie attributes
           `extend' if non-zero, session will be extended if
                `extend' or less seconds left in session time to live
           `title' is optional title for login screen"""
        CookieAuth.__init__(self, name, fields, pwfile, salt, ttl,
                            logger, cookie_attrs, title)
        StatelessAuthMixin.__init__(self, name, fields, pwfile, ttl, title)

class SessionHiddenAuth(SessionAuthMixin, HiddenAuth):
    """hidden field based authentication using session identifier.
       session identifier is a uuid, passed in a hidden field in the
       user's form and must be looked up in a disk-based cache of
       sessions."""
    def __init__(self, name, fields, pwfile, field_name, session_dir,
                 salt=None, ttl=DEFTTL, logger=None, extend=0,
                 cookie_attrs=None, title=None):
        """`name' is application name, user for cookie, printed on login screen
           `fields' are CGI fields from `cgiFieldStorage()'
           `pwfile' is PWFile object, must be CGI readable
           `field_name' is name of hidden field w/ authenticator data
           `session_dir' is directory for session data storage
                (must be CGI writable)
           `salt' is application specific salt string
                (if not supplied, will be fetched from password file)
           `ttl' is time-to-live for session (in seconds); zero means endless
           `logger' if supplied, is a logger object (ala `logging' module)
           `extend' if non-zero, session will be extended if
                `extend' or less seconds left in session time to love
           `cookie_attrs' is optional dictionary of cookie attributes
           `title' is optional title for login screen"""
        HiddenAuth.__init__(self, name, fields, pwfile, salt, field_name,
                            ttl, logger, title)
        SessionAuthMixin.__init__(self, name, fields, session_dir, ttl, extend)

class StatelessHiddenAuth(StatelessAuthMixin, HiddenAuth):
    """Stateless hidden field based authentication;
       User supplied hidden field contains: user/time/hash(hashedpw,time);
       Does not depend on server state data,
       BUT exposes user names (unless encyption methods overridden),
       Requires password file lookup on each authentication."""
    def __init__(self, name, fields, pwfile, field_name,
                 salt=None, ttl=DEFTTL, logger=None, cookie_attrs=None,
                 extend=0, title=None):
        """`name' is application name, user for cookie, printed on login screen
           `fields' are CGI fields from `cgi.FieldStorage()'
           `pwfile' is PWFile object, must be CGI readable
           `field_name' is name of hidden field w/ authenticator data
           `salt' is application specific salt string
                (if not supplied, will be fetched from password file)
           `ttl' is time-to-live for session (in seconds); zero means endless
           `logger' if supplied, is a logger object (ala `logging' module)
           `cookie_attrs' is optional dictionary of cookie attributes
           `extend' if non-zero, session will be extended if
                `extend' or less seconds left in session time to live
           `title' is optional title for login screen"""
        HiddenAuth.__init__(self, name, fields, pwfile, field_name,
                            salt, ttl, logger, title)
        StatelessAuthMixin.__init__(self, name, fields, pwfile, ttl)

_JAVASCRIPT_CODE = '''
// must match CGI 'make_hashed_password'
function make_hashed_password(user, password, salt) {
    var h1 = hex_hmac_sha1(password, user);
    return hex_hmac_sha1(h1, salt);
}
// must match CGI 'hashpwn'
function hashpwn(hpw, nonce) {
    return hex_hmac_sha1(hpw, nonce);
}
function submit_hook(form) {
//    if (!form.user.value || !form.password.value) {
//        alert("must have user and password");
//        return false;
//    }
    var hpw = make_hashed_password(form.user.value, form.password.value, form.salt.value);
    form.hashedpw.value = hashpwn(hpw, form.nonce.value);
    form.salt.value = "";
    form.password.value = "";
    return true;
}

// stripped of comments, unused functions.  see URL below for full version.
// slashslash comments removed, slashstar comments passed thru
/* JavaScript SHA1 by Paul Johnston pajhome.org.uk/crypt/uk */
//
// A JavaScript implementation of the Secure Hash Algorithm, SHA-1, as defined
// in FIPS PUB 180-1
// Version 2.1a Copyright Paul Johnston 2000 - 2002.
// Other contributors: Greg Holt, Andrew Kepert, Ydnar, Lostinet
// Distributed under the BSD License
// See http://pajhome.org.uk/crypt/md5 for details.

var chrsz   = 8;
function hex_hmac_sha1(key, data){ return binb2hex(core_hmac_sha1(key, data));}

function core_sha1(x, len)
{
  x[len >> 5] |= 0x80 << (24 - len % 32);
  x[((len + 64 >> 9) << 4) + 15] = len;

  var w = Array(80);
  var a =  1732584193;
  var b = -271733879;
  var c = -1732584194;
  var d =  271733878;
  var e = -1009589776;

  for(var i = 0; i < x.length; i += 16)
  {
    var olda = a;
    var oldb = b;
    var oldc = c;
    var oldd = d;
    var olde = e;

    for(var j = 0; j < 80; j++)
    {
      if(j < 16) w[j] = x[i + j];
      else w[j] = rol(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1);
      var t = safe_add(safe_add(rol(a, 5), sha1_ft(j, b, c, d)),
                       safe_add(safe_add(e, w[j]), sha1_kt(j)));
      e = d;
      d = c;
      c = rol(b, 30);
      b = a;
      a = t;
    }

    a = safe_add(a, olda);
    b = safe_add(b, oldb);
    c = safe_add(c, oldc);
    d = safe_add(d, oldd);
    e = safe_add(e, olde);
  }
  return Array(a, b, c, d, e);

}

function sha1_ft(t, b, c, d)
{
  if(t < 20) return (b & c) | ((~b) & d);
  if(t < 40) return b ^ c ^ d;
  if(t < 60) return (b & c) | (b & d) | (c & d);
  return b ^ c ^ d;
}

function sha1_kt(t)
{
  return (t < 20) ?  1518500249 : (t < 40) ?  1859775393 :
         (t < 60) ? -1894007588 : -899497514;
}

function core_hmac_sha1(key, data)
{
  var bkey = str2binb(key);
  if(bkey.length > 16) bkey = core_sha1(bkey, key.length * chrsz);

  var ipad = Array(16), opad = Array(16);
  for(var i = 0; i < 16; i++)
  {
    ipad[i] = bkey[i] ^ 0x36363636;
    opad[i] = bkey[i] ^ 0x5C5C5C5C;
  }

  var hash = core_sha1(ipad.concat(str2binb(data)), 512 + data.length * chrsz);
  return core_sha1(opad.concat(hash), 512 + 160);
}

function safe_add(x, y)
{
  var lsw = (x & 0xFFFF) + (y & 0xFFFF);
  var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
  return (msw << 16) | (lsw & 0xFFFF);
}

function rol(num, cnt)
{
  return (num << cnt) | (num >>> (32 - cnt));
}

function str2binb(str)
{
  var bin = Array();
  var mask = (1 << chrsz) - 1;
  for(var i = 0; i < str.length * chrsz; i += chrsz)
    bin[i>>5] |= (str.charCodeAt(i / chrsz) & mask) << (32 - chrsz - i%32);
  return bin;
}

function binb2hex(binarray)
{
  var hex_tab = "0123456789abcdef";
  var str = "";
  for(var i = 0; i < binarray.length * 4; i++)
  {
    str += hex_tab.charAt((binarray[i>>2] >> ((3 - i%4)*8+4)) & 0xF) +
           hex_tab.charAt((binarray[i>>2] >> ((3 - i%4)*8  )) & 0xF);
  }
  return str;
}
'''

# tools for hashed password management;

def make_hashed_password(user, password, salt):
    """returns hash of `user', `password' and application specific `salt'
       (makes same user/password pair hash differently for different apps)
       suitable for storage in an password file, or passed to `hashpwn()'.
       NOTE: MUST perform same operations
       as JavaScript `make_hashed_password()' function!"""
    hash1 = hmac.new(password, user, hashlib.sha1)
    return hmac.new(hash1.hexdigest(), salt, hashlib.sha1).hexdigest()

def hashpwn(hashedpw, nonce):
    """Return hash of hashed password (from `make_hashed_password') and nonce.
       NOTE: MUST perform same operations as JavaScript `hashpwn()' function"""
    return hmac.new(hashedpw, str(nonce), hashlib.sha1).hexdigest()

def check_hashed_password(response, nonce, refpw):
    """Check if hashed password `response' returned from login form `hashpwn()'
       function matches hash of `refpw' (from password file) and nonce."""
    return refpw and response == hashpwn(refpw, nonce)

class PWFile(object):
    """Object for retrieving password file entries"""
    def __init__(self, password_file):
        self.password_file = password_file

    def exists(self):
        """test if password file exists"""
        return os.path.isfile(self.password_file)

    def get_hashed_password(self, user):
        """Fetch hashed password for `user'"""
        if not os.path.isfile(self.password_file):
            return None
        pwf = file(self.password_file)
        start = user + ':'
        ret = None
        for line in pwf:
            if line.startswith(start):
                items = line.strip("\n").split(':')
                ret = items[1]
                break
        pwf.close()
        return ret

def cgi_test():
    """here if cgiauth.py invoked as a CGI script;
       expects: /tmp/pwfile (CGI readable password file)
                /tmp/sessions (CGI writable directory)
                able to create: /tmp/authlog"""
    import cgitb
    cgitb.enable()
    import cgi
    import logging

    fields = cgi.FieldStorage()

    logger = logging.getLogger(os.path.basename(sys.argv[0]))
    logger.setLevel(logging.DEBUG)
    chan = logging.FileHandler("/tmp/authlog")
    chan.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    chan.setFormatter(formatter)
    logger.addHandler(chan)

    pwfile = '/tmp/pwfile'
    name = 'test'
    title = "CGIAuth Test"

    test_type = fields.getfirst('type')
    if not test_type:
        # look at cookie... ooof!
        cookie_string = os.environ.get('HTTP_COOKIE')
        if cookie_string:
            cookies = Cookie.SimpleCookie()
            cookies.load(cookie_string)
            if cookies.get(name):
                cookie = cookies[name].value
                if cookie.find('-') == -1:
                    test_type = 'stateless'
        if not test_type:
            test_type = 'session'

    # add extra row for test type!
    def button(btype):
        """return text for a radio button"""
        if btype == test_type:
            checked = ' checked'
        else:
            checked = ''
        return '%s: <input name="type" type="radio" value="%s"%s> ' % \
                (btype, btype, checked)

    extra_row = '<tr><td><b>Test:</b><td>' + \
        button('session') + button('stateless') + button('basic')

    if test_type == 'session':
        sessdir = '/tmp/sessions'
        if not os.path.isdir(sessdir):
            os.mkdir(sessdir)
        # GAK! should subclass!
        SessionCookieAuth.EXTRA_ROWS = extra_row
        auth = SessionCookieAuth(name, fields, PWFile(pwfile),
                                 sessdir, logger=logger, title=title)
    elif test_type == 'stateless':
        # override encrypt/decrypt for test/demo?
        # GAK! should subclass!
        StatelessCookieAuth.EXTRA_ROWS = extra_row
        auth = StatelessCookieAuth(name, fields, PWFile(pwfile),
                                   logger=logger, title=title)
    else:
        auth = BasicAuth(name, logger=logger)

    auth.content_html()
    print '''<html>
<head><title>logged in</title></head>
<body>'''
    print "Time:", time.time()
    print '<br>'
    print "User:", auth.user
    print '<br>'
    print "Cookies:", os.environ.get('HTTP_COOKIE')

    if hasattr(auth, 'logout_url'):
        print '<br>'
        print '<a href="%s">LOGOUT</a>' % auth.logout_url()

    if hasattr(auth, 'logout_button'):
        print auth.logout_button()

    cgi.print_form(fields)
    cgi.print_environ()

    print '</body>'
    print '</html>'

def set_password():
    """create/change password file entries when invoked from command line"""
    import getpass

    if len(sys.argv) != 2:
        sys.stderr.write("Usage: %s password_file\n" % sys.argv[0])
        sys.exit(1)
    pwfname = sys.argv[1]
    pwfile = PWFile(pwfname)
    
    # crock -- just for now???
    salt = pwfile.get_hashed_password(SALTUSER)
    # XXX check return!

    sys.stderr.write("Username: ")
    user = sys.stdin.readline().strip("\n")
    if not user:
        sys.exit(1)
    # check for rational username?
    if user.find(':') != -1:
        sys.stderr.write("Bad username\n")
        sys.exit(1)
    password = getpass.getpass()

    # XXX move to PWFile.set_password(user, password) ???
    if pwfile.get_hashed_password(user):
        hashed = make_hashed_password(user, password, salt)

        # hard case: need to re-write file
        start = user + ':'
        orig = file(pwfname)
        tmpfile = pwfile + '.tmp'
        tmp = file(tmpfile, 'w')
        for line in orig:
            if line.startswith(start):
                tmp.write('%s:%s\n' % (user, hashed))
            else:
                tmp.write(line)
        orig.close()
        tmp.close()
        # save old file?
        os.rename(tmpfile, pwfile)
    else:
        # no old password: just append
        pwf = file(pwfname, 'a')
        if not salt:
            # if no salt entry, create one!
            # use host-based uuid1?
            salt = str(uuid.uuid4())
            pwf.write("%s:%s\n" % (SALTUSER, salt))
        # create hash now that we have a salt!
        hashed = make_hashed_password(user, password, salt)
        pwf.write('%s:%s\n' % (user, hashed))
        pwf.close()

if __name__ == '__main__':
    if os.environ.get("REMOTE_ADDR"):
        cgi_test()
    else:
        set_password()
