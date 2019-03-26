import pytest

from pymlconf import Root


class MyWriter:
    pass


class Test:

    _builtin = '''
    app:
        name: MyApp
        listen:
            sock1:
                addr: 192.168.0.1
                port: 8080
            sock2:
                addr: 127.0.0.1
                port: "89"
        languages:
            - english
            - {language: persian, country: iran}


    logging:
        logfile: /var/log/myapp.log
        formatter: !!python/name:str
        writer: !!python/object:%s.MyWriter {}
    ''' % __name__

    def test_simple_syntax(self):
        """
        Testing simple Yaml syntax
        """

        cm = Root(self._builtin)
        assert cm.app.name == 'MyApp'
        assert len(cm.app.listen) == 2
        assert cm.app.listen.sock1.addr == '192.168.0.1'
        assert cm.app.listen.sock1.port == 8080
        assert cm.app.listen.sock2.addr == '127.0.0.1'
        assert cm.app.listen.sock2.port == '89'
        assert cm.logging.logfile == '/var/log/myapp.log'

        assert len(cm.app.languages) == 2
        assert cm.app.languages[0] == 'english'
        assert cm.app.languages[1].language == 'persian'
        assert cm.app.languages[1].country == 'iran'
        assert cm.logging.formatter == str
        assert isinstance(cm.logging.writer, MyWriter)

