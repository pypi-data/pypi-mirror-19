from collections import OrderedDict
from itertools import chain


dialect = 'standard'


def build_where_expr(conditions=[], keyword='WHERE'):
    if not conditions:
        return '', []

    if isinstance(conditions, (int, long)):
        conditions = [{'id =': conditions}]

    if isinstance(conditions, dict):
        conditions = [conditions]

    conditions = [OrderedDict(condition) for condition in conditions]

    def build_single_comparation(predicate, value):
        if ' ' in predicate:
            field, op = predicate.split(' ')
        else:
            field, op = predicate, '='

        if op == 'in' and isinstance(value, list):
            placeholders = '(' + ','.join(['%s'] * len(value)) + ')'
        else:
            placeholders = '%s'

        return '%s %s %s' % (quote_identifier(field),
                             validate_operator(op),
                             placeholders)

    def build_comparation_group(cond):
        return ' AND '.join(build_single_comparation(predicate, value)
                               for predicate, value in cond.items())

    def flatten(inlist):
        outlist = []

        for item in inlist:
            if isinstance(item, list):
                outlist.extend(item)
            else:
                outlist.append(item)

        return outlist

    tpl = ' OR '.join(['(%s)' % build_comparation_group(cond) for cond in conditions])

    values = list(chain(*(flatten(cond.values()) for cond in conditions)))

    return '%s %s' % (keyword, tpl), values


def quote_identifier(identifier):
    templates = {'standard': '"%s"',
                 'postgresql': '"%s"',
                 'mysql': '`%s`',
                 'mssql': '[%s]'}

    return templates[dialect] % identifier


def validate_operator(op):
    supported_operators = (
        '=', '>', '<', '!=', '<=', '>=', 'in'
    )

    if op not in supported_operators:
        raise ValueError('Non supported operator!')

    return op


if __name__ == '__main__':
    expr = build_where_expr([{'id': 5, 'value >': 7}, {'yarak in': ['siksok', 'am']}])
    print expr
    pass
