# coding: utf8


class RowDict(dict):
    """
    object support __getitem__ and __getattr__
    """

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value


class MysqlEngineWithOursql(object):
    def __init__(self, engine):
        if isinstance(engine, (basestring, str,)):
            from sqlalchemy import create_engine
            self.engine = create_engine(engine)
        else:
            self.engine = engine

    @staticmethod
    def translate_in_stmt(sql, args):
        """
        translate in stmt to oursql qmark format
        eg:
            ` select * from table where id in %s  ,  ((10, 20, 30,)) `
            will translate to
            ` select * from table where id in (?, ?, ?)   , (10, 20, 30,)

        :param sql:
        :param args:
        :return:
        """
        in_stmt_placeholders = []
        smart_args = []
        for arg in args:
            if isinstance(arg, (list, tuple)):
                in_stmt_placeholders.append('(' + ','.join(['?' for x in arg]) + ')')
                for x in arg:
                    assert not isinstance(x, (list, tuple)), "list cannot be nested"
                    smart_args.append(x)
            else:
                smart_args.append(arg)
        if len(in_stmt_placeholders) == 0:
            return sql, args
        smart_sql = sql % tuple(in_stmt_placeholders)
        print smart_sql
        return smart_sql, smart_args

    def _raw_fetch(self, sql, args):
        return self.engine.execute(*self.translate_in_stmt(sql, args))

    def fetch(self, sql, args):
        res = self._raw_fetch(sql, args)
        if not res:
            return []
        return res.fetchall()

    def fetch_row(self, sql, args):
        res = self._raw_fetch(sql, args)
        if not res:
            return res
        li = []
        keys = res.keys()
        lower_keys = [x.lower() for x in keys]
        for row in res:
            origin = dict(zip(keys, row))
            lower = dict(zip(lower_keys, row))
            origin.update(lower)
            li.append(RowDict(origin))
        return li

    def fetchone(self, sql, args):
        res = self.fetch(sql, args)
        if not res:
            return None
        assert len(res) == 1, "call fetchone, but result size is %s" % len(res)
        return res[0]

    def fetchone_row(self, sql, args):
        res = self.fetch_row(sql, args)
        if not res:
            return None
        assert len(res) == 1, "call fetchone, but result size is %s" % len(res)
        return res[0]

    def __getattr__(self, item):
        # fall back to engine
        return getattr(self.engine, item)


MysqlEngine = MysqlEngineWithOursql
