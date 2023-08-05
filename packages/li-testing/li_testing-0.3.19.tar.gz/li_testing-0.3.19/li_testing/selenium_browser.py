# -*- coding: utf-8 -*-
"""This module implements a simple test browser using selenium."""

import datetime
import logging
import time
from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import six


class SeleniumBrowserMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # methods that should not be wrapped
        non_wrappable = ['send_screenshot']

        for name, value in attrs.items():
            # we don't wrap magic methods this is why the startswith is here.
            if callable(value) and not name.startswith('__') \
               and name not in non_wrappable:
                attrs[name] = cls.send_screenshot_wrapper(value)

        return super(SeleniumBrowserMetaclass, cls).__new__(
            cls, name, bases, attrs)

    @classmethod
    def send_screenshot_wrapper(cls, func):

        def wrapper(self, *args, **kwargs):
            try:
                r = func(self, *args, **kwargs)
            except Exception as e:
                if self.send_screenshot_on_error:
                    self.send_screenshot()
                raise e

            return r

        return wrapper


class SeleniumBrowserException(Exception):
    pass


class SeleniumBrowser(six.with_metaclass(SeleniumBrowserMetaclass,
                                         webdriver.Chrome)):
    """Um browser simples para testes de aceitação usando o
    selenium Chrome webdriver."""

    def __init__(self, send_screenshot_on_error=False, aws_access_key=None,
                 aws_secret_key=None, bucket_name=None, vcs_commit=None):
        """Contrutor para o SeleniumBrowser.

        :param send_screenshot_on_error: Indica se uma captura de tela
          deve ser enviada a um bucket s3 em caso de erro.
        :param aws_access_key: Chave de acesso ao s3.
        :param aws_secret_key: Chave secreta para acesso ao s3.
        :param bucket_name: O nome do bucket no s3.
        :param vcs_commit: Identificador do commit no vcs."""

        super(SeleniumBrowser, self).__init__()
        self.maximize_window()
        self.send_screenshot_on_error = send_screenshot_on_error
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.bucket_name = bucket_name
        self.vcs_commit = vcs_commit
        self.s3conn = None

    def _get_bucket_key(self):
        """Retorna uma chave para ser usada no bucket baseada num commit
        no git. Se um repositório git não existe para o código o placeholder
        <no-vcs> é usado.
        """

        commit = self.vcs_commit or '<no-vcs>'
        now = datetime.datetime.now()
        fnow = now.strftime('%Y/%m/%d/%H-%M-%S')
        key = '{}/{}-selenium_error.png'.format(commit, fnow)
        return key

    def _connect2s3(self):
        """Cria uma nova conexão com o s3."""

        if not (self.aws_access_key and self.aws_secret_key):
            raise SeleniumBrowserException(
                'No aws credentials to connect to s3')

        self.s3conn = S3Connection(self.aws_access_key, self.aws_secret_key,
                                   calling_format=OrdinaryCallingFormat())

    def send_screenshot(self):
        """Pega uma captura de tela do selenium e envia para um
        bucket no s3."""

        if not self.s3conn:
            self._connect2s3()

        key = self._get_bucket_key()
        msg = 'logging selenium error at {}'.format(key)
        logging.log(logging.ERROR, msg)
        shot = self.get_screenshot_as_png()
        bucket = self.s3conn.get_bucket(self.bucket_name)
        bucket_key = bucket.new_key(key)
        bucket_key.set_contents_from_string(shot)

    def wait_text_become_present(self, text, timeout=20):
        """Espera até que um texto esteja presente no código da página.

        :param text: O texto que deverá estar presente na página.
        :param timeout: timeout em segundos para a operação."""

        r = int(timeout * 10)

        for index in range(r):
            time.sleep(0.1)
            if text in self._get_source():
                return True

        raise SeleniumBrowserException(
            'text %s not present after %s seconds' % (text, timeout))

    def wait_element_become_visible(self, el, timeout=20):
        """Espera até que um elemento seja visível na página.

        :param el: Um elemento da página
        :param timeout: Timeout para a operação."""

        r = int(timeout * 10)

        for index in range(r):
            time.sleep(0.1)
            if el.is_displayed():
                return True

        raise SeleniumBrowserException(
            'The element %s not visible after %s seconds' % (el, timeout))

    def hover(self, element):
        """Passa o mouse por cima de um elemento

        :param element: O elemento em questão."""

        hover = ActionChains(self).move_to_element(element)
        hover.perform()

    def click(self, element):
        """Clica num elemento usando ActionChain.

        :param element: Um elemento para clicar."""

        action = ActionChains(self).click(element)
        action.perform()

    def _get_source(self):  # pragma no cover
        """Returns the source code of the current page."""

        return self.page_source
