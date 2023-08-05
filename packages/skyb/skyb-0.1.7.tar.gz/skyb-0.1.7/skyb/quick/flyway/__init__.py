# coding: utf8

__author__ = 'fyz'

import os
import os.path
import sys
import glob
import hashlib
from functools import total_ordering
import argparse
from ...utils import cur_ms
from ...conf.conf_loader import load_configuration, ConfigurationContext

from sqlalchemy import create_engine

SCHEMA_TABLE = """
    CREATE TABLE IF NOT EXISTS `schema_version` (
      `version` int(11) PRIMARY KEY,
      `script` varchar(512) NOT NULL,
      `checksum` varchar(64) DEFAULT NULL,
      `time_created` bigint(20) NOT NULL,
      `execution_time` int(11) NOT NULL,
      `status` int(11) NOT NULL DEFAULT 0
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
"""


def info(msg):
    print "INFO %s" % msg


def error(msg):
    print "\033[91mERROR %s\033[0m" % msg


def prompt(msg, cb, *args, **kw):
    res = raw_input(msg + " [Y/N]: ")
    if res.lower() == 'y':
        cb(*args, **kw)


DEFAULT_CONFIG = {
    "ignore_order": False,
    "pattern": "V*.sql"
}


@total_ordering
class Script(object):
    PREFIX = 'V'
    MAGIC_NUMBER = 100000
    VERSION_SPLITTER = "__"

    def __init__(self, location=None, version=None, checksum=None, filename=None, context=None):
        self.context = context
        self.location = location
        self.content = None
        self.filename = filename
        if self.location is not None:
            assert os.path.isfile(self.location), "script location must be file, %s" % location
            _, self.filename = os.path.split(self.location)
            self.original_version, self.version = self.extract_version()
            self.load_content()
        else:
            assert version is not None
            self.version = version
            self.original_version = self.from_magic_version(self.version)
            self.checksum = checksum

    def extract_version(self):
        version, description = self.filename.split(self.VERSION_SPLITTER, 1)
        assert version.startswith(self.PREFIX), "filename should start with %s" % self.PREFIX
        assert len(description) > 0
        original_version = version[1:]
        return original_version, self.generate_magic_version(original_version)

    @staticmethod
    def generate_magic_version(original_version):
        return int(float(original_version) * Script.MAGIC_NUMBER)

    @staticmethod
    def from_magic_version(version):
        return str(version / float(Script.MAGIC_NUMBER))

    @staticmethod
    def calculate_checksum(content):
        m2 = hashlib.md5()
        m2.update(content)
        return m2.hexdigest()

    def load_content(self):
        with open(self.location, 'r') as fp:
            content = '\n'.join(fp.readlines())
            self.content = content
            self.checksum = self.calculate_checksum(self.content)

    def __eq__(self, other):
        return self.version == other.version and self.checksum == other.checksum

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.version < other.version

    def __str__(self):
        return '[ Script %s %s ]' % (self.version, self.filename)

    __repr__ = __str__


class MigrationContext(object):
    LIST_SQL = "select * from schema_version order by version"
    INSERT_SQL = """insert into schema_version values ('%s', '%s', '%s', %s, 0, 0)"""
    INSTALL_SUCCESS_SQL = '''update schema_version set `status` = 1, execution_time=%s where `version` = %s'''
    LIST_UNFINISHED_SQL = '''select version, script, time_created from schema_version where `status` = 0'''

    def __init__(self, cmd, args, config):
        self.cmd = cmd
        self.args = args
        self.config = config

        self.location = config.get('location')
        self.pattern = config.get('pattern')

        self._init_table()

        self._check_unfinished_script()

    def _init_table(self):
        self.engine = create_engine(self.config.get('url'))
        self.engine.execute(SCHEMA_TABLE)

    def _check_unfinished_script(self):
        scripts = self.engine.execute(self.LIST_UNFINISHED_SQL)
        if scripts and scripts.rowcount > 0:
            error("found unfinished scripts")
            for s in scripts:
                error("%s, %s" % (s[0], s[1],))
            sys.exit(1)


    def execute(self):
        self.cmd = self.cmd.replace('-', '_')
        method = getattr(self, "handle_" + self.cmd, None)
        assert method is not None, "No Command <%s>" % self.cmd
        method()

    ##############################################################
    ###########             CMD SECTION            ###############
    ##############################################################

    def handle_list_config(self):
        assert len(self.args) == 0, "arguments error"
        for k, v in self.config.get_inner_value().iteritems():
            print k, v

    def handle_list_scripts(self):
        assert len(self.args) == 0, "arguments error"
        scripts = self._list_all_scripts()
        for s in scripts:
            print s

    def handle_list_installed_scripts(self):
        assert len(self.args) == 0, "arguments error"
        scripts = self._list_installed_scripts()
        for s in scripts:
            print s

    def handle_list_uninstall_scripts(self):
        all_scripts = self._list_all_scripts()
        installed_scripts = self._list_installed_scripts()
        uninstall_scripts = [x for x in all_scripts if x not in installed_scripts]
        for s in uninstall_scripts:
            print s

    def handle_validate(self):
        all_scripts = self._list_all_scripts()
        installed_scripts = self._list_installed_scripts()
        for s in installed_scripts:
            if s not in all_scripts:
                print 'INVALID', s

    def handle_install(self):
        installed_scripts = self._list_installed_scripts()
        versions = [Script.generate_magic_version(x) for x in self.args]
        i_scripts = self._find_script(installed_scripts, *versions)
        has_error = False
        if len(i_scripts) > 0:
            for k, v in i_scripts:
                if v is not None:
                    has_error = True
                    error("%s has been installed" % v.filename)
        if has_error:
            sys.exit(1)

        all_scripts = self._list_all_scripts()
        u_scripts = self._find_script(all_scripts, *versions)
        for k, v in u_scripts:
            if v is None:
                has_error = True
                error("version %s file not exist" % Script.from_magic_version(k))
        if has_error:
            sys.exit(1)

        for k, v in u_scripts:
            prompt("install %s ?" % v.filename, self._install_script, v)

    def handle_migrate(self):
        info("MIGRATE BEGIN")
        installed_scripts = self._list_installed_scripts()
        all_scripts = self._list_all_scripts()
        uninstall_scripts = [x for x in all_scripts if x not in installed_scripts]
        if not self.config.get("ignore_order"):
            self._check_order(installed_scripts, uninstall_scripts)
        assert len(installed_scripts) + len(uninstall_scripts) == len(all_scripts)

        self._install_script(uninstall_scripts)
        info("MIGRATE END, INSTALL %s SCRIPTS" % len(uninstall_scripts))

    ##############################################################
    ###########             CMD SECTION            ###############
    ##############################################################

    @staticmethod
    def _check_script_version_duplicate(scripts):
        if len(scripts) < 2:
            return
        for i in range(len(scripts) - 1):
            assert scripts[i].version != scripts[i + 1].version, \
                "duplicate script version, %s, %s" % (scripts[i].filename, scripts[i + 1].filename,)

    def _list_all_scripts(self):
        current_dir = os.getcwd()
        abs_location = os.path.abspath(os.path.join(current_dir, self.location))
        assert os.path.isdir(abs_location), "location should be a directory"

        os.chdir(abs_location)
        script_files = glob.glob(self.pattern)
        os.chdir(current_dir)

        if len(script_files) == 0:
            return []
        scripts = [Script(location=os.path.join(abs_location, x), context=self) for x in script_files]
        scripts.sort()
        self._check_script_version_duplicate(scripts)
        return scripts

    def _list_installed_scripts(self):
        res = self.engine.execute(self.LIST_SQL)
        if not res:
            return []
        installed_scripts = []
        for row in res:
            tmp = dict(zip(res.keys(), row))
            installed_scripts.append(
                Script(version=tmp['version'], checksum=tmp['checksum'], filename=tmp['script'], context=self))
        installed_scripts.sort()
        return installed_scripts

    def _execute_script(self, script):
        info("install script BEGIN: %s" % script)
        begin_time = cur_ms()

        begin_sql = self.INSERT_SQL % (
            script.version, script.filename, script.checksum, cur_ms())
        self.engine.execute(begin_sql)

        content = script.content.strip().strip(";")
        contents = content.split(";")
        for c in contents:
            c = c.strip()
            if len(c) > 0:
                self.engine.execute(c)
        finish_sql = self.INSTALL_SUCCESS_SQL % (cur_ms() - begin_time, script.version,)
        self.engine.execute(finish_sql)

    @staticmethod
    def _check_order(s1, s2):
        if len(s1) == 0 or len(s2) == 0:
            return

        assert s1[-1].version < s2[0].version, "version not in order, %s not install, but %s has been installed" % (
            s2[0].filename, s1[-1].filename)

    def _install_script(self, script):
        if isinstance(script, list):
            for single_script in script:
                self._install_script(single_script)
        else:
            self._execute_script(script)

    @staticmethod
    def _find_script(scripts, *versions):
        if len(versions) == 0:
            return []
        result = []
        for version in versions:
            found = False
            for script in scripts:
                if script.version == version:
                    result.append((version, script,))
                    found = True
                    break
            if not found:
                result.append((version, None,))
        return result


def main():
    parser = argparse.ArgumentParser(
        description="Python Version Of Flyway. Dependencies: sqlalchemy, oursql/mysql-connector")
    parser.add_argument('cmd', nargs='+', help="command")
    parser.add_argument('--url', help="database url \n \tformat: mysql+oursql(mysqlconnector)://user:pw@host/dbname")
    parser.add_argument('--location', help="script files location")
    parser.add_argument('--pattern', help="script file pattern")
    parser.add_argument('--ignore_order', action="store_true", help="whether to ignore script order")
    parser.add_argument('--config', '-c', help="config file location")

    cmd_conf, _ = parser.parse_known_args()
    cmd = cmd_conf.cmd

    if cmd_conf.config is not None:
        conf = load_configuration(filename=cmd_conf.config)
    else:
        conf = ConfigurationContext()
    for k, v in cmd_conf.__dict__.iteritems():
        if v is not None and k != 'cmd':
            conf.fill_kv(k, v)

    conf.fill_dict(DEFAULT_CONFIG, only_absent=True).lock()

    MigrationContext(cmd[0], cmd[1:], conf).execute()
