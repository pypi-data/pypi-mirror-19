# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.test.testcases import LiveServerThread


class LiveTestServer(LiveServerThread):
    """Um servidor para ser usado nos testes de aceitação. Você precisa
    iniciar o servidor antes dos seus testes e matá-lo quando os testes
    terminarem.

    Modo de uso
    ===========

    from li_testing.liveserver import LiveTestServer

    server = LiveTestServer()
    server.start()

    # To get the url that is being served, use:
    server.live_server_url

    # do your tests stuff
    # ...
    server.stop()
    """

    def __init__(self):
        self.host = 'localhost'
        if hasattr(settings, 'TEST_SERVER_PORT') and settings.TEST_SERVER_PORT:
            self.port = settings.TEST_SERVER_PORT
        else:
            self.port = 8001
        self.static_handler = StaticFilesHandler
        super(LiveTestServer, self).__init__(self.host, [self.port],
                                             self.static_handler)
        self.daemon = True

    def start(self):
        """Inicia o servidor."""

        super(LiveTestServer, self).start()
        self.is_ready.wait()

    @property
    def live_server_url(self):
        """Url sendo usada pelo servidor."""
        return 'http://%s:%s' % (self.host, self.port)

    def stop(self):
        """Mata o servidor."""

        self.terminate()
        self.join()
