import os
import re
from pymlconf import ConfigDict, ConfigManager
from pymlconf.compat import TestCase, _CompatTestCase
from pymlconf.config_manager import ERROR, IGNORE
from pymlconf.errors import ConfigFileNotFoundError

this_dir = os.path.abspath(os.path.dirname(__file__))
conf_dir = os.path.abspath(os.path.join(this_dir, 'conf'))


class TestConfigManager(TestCase, _CompatTestCase):
    def setUp(self):
        self.initial_config = {
            'version': 2.5,
            'general': {'name': 'albatross'},
            'domains': ConfigDict({'coldon_ir': ConfigDict(), 'fangtooth_ir': ConfigDict({'name': 'fangtooth'})}),
            'data': {'url': 'some uri'}  # without ConfigDict
        }

    def test_builtins(self):
        a_date = '2014/12/01'

        builtin = """
        builtin:
          value1: built-in config value
        """

        cm = ConfigManager(builtin=builtin, init_value=self.initial_config, context=dict(date=a_date))
        self.assertEqual(cm.builtin.value1, 'built-in config value')
        cm.merge("""
a_date: %(date)s
        """)
        self.assertEqual(cm.version, 2.5)
        cm.version = 2.6
        self.assertEqual(cm.version, 2.6)
        self.assertEqual(cm.a_date, a_date)
        self.assertEqual(cm.general.name, self.initial_config['general']['name'])
        self.assertIsInstance(cm.domains['coldon_ir'], ConfigDict)
        self.assertEqual(cm.data.url, 'some uri')

    def test_files(self):

        # noinspection PyUnresolvedReferences
        files = [os.path.join(conf_dir, '../files', 'c111.conf'),
                 os.path.join(conf_dir, '../files', 'something-that-not-exists.conf')]
        cm = ConfigManager(init_value=self.initial_config, dirs=[conf_dir], files=files)

        # root.conf
        self.assertEqual(cm.version, 2.5)
        self.assertEqual(cm.domains.coldon_ir.name, 'coldon')
        self.assertEqual(cm.general.tcp_port, 5671)

        # general.conf
        self.assertEqual(cm.general.name, 'Vahid')
        self.assertEqual(cm.domains['fangtooth_ir'].name, 'Fangtooth2')

        # domains_coldon.ir.conf
        self.assertEqual(cm.domains['coldon_ir'].path, '/home/local/coldon')

        # domains_dobisel.com.conf
        self.assertEqual(cm.domains['dobisel_com'].path, '/home/local/dobisel')
        self.assertEqual(cm.domains['dobisel_com'].name, 'dobisel')
        self.assertEqual(cm.domains['dobisel_com'].applications.app1.name, 'app1')
        self.assertEqual(cm.domains['dobisel_com'].applications.app2.users.vahid.fullname, 'Vahid Mardani')
        self.assertEqual(cm.domains['dobisel_com'].applications.app2.users.vahid.password, 'himopolxx')
        self.assertEqual(cm.baghali, 2)
        # builtins
        self.assertEqual(cm.data.url, 'some uri')

    def test_non_existence_file(self):
        # noinspection PyUnresolvedReferences
        files = [os.path.join(conf_dir, '../files', 'c111.conf'),
                 os.path.join(conf_dir, '../files', 'something-that-not-exists.conf')]

        import logging
        import sys
        from pymlconf.compat import StringIO

        logger = logging.getLogger('pymlconf')
        logger.level = logging.DEBUG
        saved_stdout = sys.stdout
        saved_stderr = sys.stderr

        sys.stdout = StringIO()
        sys.stderr = StringIO()
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        try:
            # Testing ignore behavior
            ConfigManager(init_value=self.initial_config, dirs=[conf_dir], files=files,
                          missing_file_behavior=IGNORE)
            output = sys.stdout.getvalue().strip()
            self.assertNotRegexpMatches(output, "^File not found: ['\"]?(?:/[^/]+)*['\"]?$")

            # # Testing default behavior which just prints a warning
            # ConfigManager(init_value=self.initial_config, dirs=[conf_dir], files=files)
            # output = sys.stderr.getvalue().strip()
            #
            #
            # self.assertTrue(output.startswith("UserWarning: File not found:"))

            # Testing strict behavior
            self.assertRaises(ConfigFileNotFoundError, ConfigManager,
                              init_value=self.initial_config,
                              dirs=[conf_dir],
                              files=files,
                              missing_file_behavior=ERROR)

        finally:
            logger.removeHandler(stream_handler)
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr

    def test_dirs(self):
        dirs = [conf_dir]
        cm = ConfigManager(init_value=self.initial_config, dirs=dirs)

        # root.conf
        self.assertEqual(cm.version, 2.5)
        self.assertEqual(cm.domains['coldon_ir'].name, 'coldon')
        self.assertEqual(cm.general.tcp_port, 5671)

        # general.conf
        self.assertEqual(cm.general.name, 'Vahid')
        self.assertEqual(cm.domains['fangtooth_ir'].name, 'Fangtooth2')

        # domains_coldon.ir.conf
        self.assertEqual(cm.domains['coldon_ir'].path, '/home/local/coldon')

        # domains_dobisel.com.conf
        self.assertEqual(cm.domains['dobisel_com'].path, '/home/local/dobisel')
        self.assertEqual(cm.domains['dobisel_com'].name, 'dobisel')
        self.assertEqual(cm.domains['dobisel_com'].applications.app1.name, 'app1')
        self.assertEqual(cm.domains['dobisel_com'].applications.app2.users.vahid.fullname, 'Vahid Mardani')
        self.assertEqual(cm.domains['dobisel_com'].applications.app2.users.vahid.password, 'himopolxx')

        # builtins
        self.assertEqual(cm.data.url, 'some uri')

    def test_new_extension(self):
        dirs = [conf_dir]
        cm = ConfigManager(init_value=self.initial_config, dirs=dirs, extension=".yaml")

        # root.conf
        self.assertEqual(cm.run.baseurl, 'http://localhost:9090')
        self.assertEqual(cm.run.skipurlcheck, True)
        self.assertEqual(cm.type, 'selenium')

        self.assertEqual(cm.testpath, conf_dir)
        # self.assertEqual(cm.selenium.xvfb.options.server-args, '-screen 0 1024x768x24')


if __name__ == '__main__':
    unittest.main()
