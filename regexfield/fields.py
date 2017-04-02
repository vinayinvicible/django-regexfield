from __future__ import absolute_import, unicode_literals

from django.db import models
from django.db.models.lookups import IRegex, Regex
from django.db.models.sql import Query
from django.utils.inspect import get_func_args
from django.utils.translation import ugettext_lazy as _


class RegexField(models.TextField):
    empty_strings_allowed = False
    description = _('A regex object')
    default_error_messages = {
        'invalid': _("Value must be valid regex."),
    }

    def db_check(self, connection):
        check_query = Query(model=self.model)
        check_query.add_q(~models.Q(**{'{}__match'.format(self.name): "''"}))
        compiler = check_query.get_compiler(connection=connection)
        compiler.pre_sql_setup()
        if hasattr(compiler, 'where'):
            where = compiler.where
        else:
            where = compiler.query.where
        sql, params = compiler.compile(where)
        return sql % tuple(params)

    # Had to override for django 1.9
    def db_parameters(self, connection):
        type_string = self.db_type(connection)
        check_string = self.db_check(connection)
        return {
            "type": type_string,
            "check": check_string,
        }


class RegexLookup(Regex):

    def process_lhs(self, compiler, connection, lhs=None, reverse=True):
        if reverse:
            self._lhs = lhs
            return self.process_rhs(
                compiler=compiler, connection=connection, reverse=not reverse
            )

        return super(RegexLookup, self).process_lhs(
            compiler=compiler, connection=connection, lhs=lhs
        )

    def process_rhs(self, compiler, connection, reverse=True):
        if reverse:
            return self.process_lhs(
                compiler=compiler, connection=connection,
                lhs=self._lhs or self.lhs, reverse=not reverse
            )

        return super(RegexLookup, self).process_rhs(
            compiler=compiler, connection=connection
        )


class IRegexLookup(RegexLookup, IRegex):
    pass


if 'lookup_name' in get_func_args(RegexField.register_lookup):
    RegexField.register_lookup(RegexLookup, lookup_name='match')
    RegexField.register_lookup(IRegexLookup, lookup_name='imatch')
else:
    if 'class_lookups' not in RegexField.__dict__:
        RegexField.class_lookups = {}
    RegexField.class_lookups['match'] = RegexLookup
    RegexField.class_lookups['imatch'] = IRegexLookup
