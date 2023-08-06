import sys

import yaml
from yamllint.linter import LintProblem

from Matcher import Matcher

ID = 'hardcoded'
TYPE = 'token'
CONF = {'password_re': str,
        'hostname_re': str}

def raise_problem(token, item_name):
    return LintProblem(token.start_mark.line, token.start_mark.column, 'Hardcoded %s' % item_name)


def check(conf, token, prev, next, nextnext, context):
    matcher = Matcher(None, conf['password_re'], conf['hostname_re'])
    if isinstance(token, yaml.tokens.ScalarToken):
        item = matcher.check(token, 'value', None)
        if item is not None:
            yield raise_problem(token, item) 




