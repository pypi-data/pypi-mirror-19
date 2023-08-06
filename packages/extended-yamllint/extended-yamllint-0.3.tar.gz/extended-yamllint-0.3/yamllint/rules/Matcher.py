import re

class Matcher:
    ''' Incapsulates string constants matching for code static analysis. '''

    EMAIL_REGEX = '(^[a-zA-Z0-9._]+@[a-z0-9._]+$)|(^[^(%s)]@[^(%s)]$)'
    # match every IP except 127.0.0.* and 0.0.0.0
    IP_REGEX = '([0-9]{1,3}\.){3}(?<!127.0.0.)[0-9]{1,3}(?<!0.0.0.0)'

    email_re = re.compile(EMAIL_REGEX)
    ip_re = re.compile(IP_REGEX)

    items = ['hostname', 'ip', 'email', 'password']

    def __init__(self, caller, password_regex, hostname_regex):
        self.hostname_re = re.compile(hostname_regex)
        self.password_re = re.compile(password_regex)
        # checker instance
        self.caller = caller
        
    def _check(self, item, s):
        return eval('self.%s_re.search(s)' % item)

    def check(self, row, field, err_fn, *args):
        """
        Takes 'field' on 'row' and runs '_check'
        on hardcoded items from 'items' list.
        If check finds hardcoded it runs 'err_fn'
        which will report on lint error for specific linter
        whose instance is stored in 'self.caller'.
        """
        for item in self.items:
            val = getattr(row, field)
            if self._check(item, val):
                if self.caller is not None:
                    err_fn(self.caller, row, item, *args)
                else:
                    return item


