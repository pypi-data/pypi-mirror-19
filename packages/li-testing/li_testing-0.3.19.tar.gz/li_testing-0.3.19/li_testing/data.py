# -*- coding: utf-8 -*-
"""Esta módulo contém funções usadas para criar conteúdo
para os testes."""

import datetime
import logging
import time
from uuid import UUID
from django.conf import settings
from django.db import connection
from django.db.models import Model
from li_common.conexoes.elasticsearch import ElasticsearchConnect
from repositories.cliente.models import ClienteGrupo
from repositories.catalogo.models import Produto
from repositories.configuracao.models import (EnvioConfiguracao, Envio,
                                              FormaPagamento,
                                              FormaPagamentoConfiguracao,
                                              EnvioFaixaCEP, EnvioRegiao,
                                              EnvioFaixaPeso)
from repositories.faturamento.models import Plano, PlanoAssinatura
from repositories.marketing.models import SEO
from repositories.plataforma.models import (Usuario, Conta, Contrato,
                                            ContaUsuario)


def create_user(email='selenium@lojaintegrada.com.br', password='12345'):
    """Cria um novo usuário lojista para ser usado nos testes.

    :param email: E-mail do usuário
    :param password: Senha do usuário
    """

    contrato = Contrato.objects.get(codigo='lojaintegrada')
    user = Usuario(email=email, confirmado=True, contrato=contrato)
    user.senha = password
    user.save()
    return user


def del_user(email='selenium@lojaintegrada.com.br'):
    """Deleta o usuário de teste.

    :param context: The behavior's context object."""

    try:
        user = Usuario.objects.get(email=email)
        user.delete()
    except Usuario.DoesNotExist:
        logging.log(logging.ERROR, 'Error deleting user on selenium tests')


def create_conta(user_email='selenium@lojaintegrada.com.br',
                 store_name='Lojinha do Selenium',
                 slug='lojinha-do-selenium'):
    """Cria uma nova conta (loja) para ser usada nos testes.

    :param user_email: O e-mail de um usuário de teste já cadastrado.
    :param store_name: Nome para a loja de teste que será criada."""

    conta = Conta(nome=store_name, apelido=slug)
    conta.wizard_finalizado = True
    conta.save()
    user = Usuario.objects.get(email=user_email)
    conta_usuario = ContaUsuario(conta=conta, usuario=user,
                                 administrador=True)
    conta_usuario.save()
    return conta, conta_usuario


def del_conta(store_name='Lojinha do Selenium'):
    """Deleta a conta criada nos testes.

    :param store_name: Nome da loja de teste a ser deletada.."""

    contas = Conta.objects.filter(nome=store_name)
    conta_user = ContaUsuario.objects.filter(conta__in=contas)
    conta_user.delete()
    # the Conta model is broken, it does not executes a delete so we
    # need to do that using SQL. :(
    query = 'DELETE FROM plataforma.tb_conta '
    query += "WHERE conta_loja_nome='%s'" % store_name
    cursor = connection.cursor()
    cursor.execute(query)


def create_plano(store_name='Lojinha do Selenium'):
    """Cria um novo plano que será usado nos testes. O plano
    criado aqui é um plano do tipo 'PRO 1'

    :param store_name: A name for the test store."""

    conta = Conta.objects.get(nome=store_name)
    plano = Plano.objects.get(nome='PRO 1')
    inicio = datetime.datetime.now()
    fim = inicio + datetime.timedelta(days=3)
    plano_assinatura = PlanoAssinatura(conta=conta, plano=plano,
                                       ciclo_inicio=inicio,
                                       ciclo_fim=fim)
    plano_assinatura.save()
    return plano_assinatura


def del_plano(store_name='Lojinha do Selenium'):
    """Deleta o plano do usuário criado nos testes.

    :param store_name: O nome da loja de testes."""

    try:
        # The thing with the filter here is that if some test has
        # failed before and could not delete some thing we delete
        # everything now.
        contas = Conta.objects.filter(nome=store_name)
        ids = [c.id for c in contas]
        PlanoAssinatura.objects.get(conta_id__in=ids).delete()
    except (PlanoAssinatura.DoesNotExist, Conta.DoesNotExist):
        msg = 'Error deleting PlanoAssinatura on selenium tests'
        logging.log(logging.ERROR, msg)


def create_product(product_name='Hacks & Stuff',
                   store_name='Lojinha do Selenium'):
    """Cria um novo produto para testes.

    :param product_name: Nome do produto a ser criado.
    :param store_name: Nome da loja que conterá o produto.
    """
    conta = Conta.objects.get(nome=store_name)
    product = Produto(nome=product_name, ativo=True, conta=conta,
                      sku='product-sku', apelido='hacks-stuff')
    product.save()
    product.estoque.situacao_em_estoque = 1
    product.estoque.save()
    product.preco.preco_cheio = 10
    product.preco.save()
    return product


def del_seo(store_name='Lojinha do Selenium'):
    """Um registro de SEO é criado automaticamente quando
    um produto é criado. Apaga este registro.

    :param store_name: Nome da loja de testes."""

    contas = Conta.objects.filter(nome=store_name)
    ids = [c.id for c in contas]
    seo = SEO.objects.filter(conta_id__in=ids)
    seo.delete()


def del_product(product_name='Hacks & Stuff',
                store_name='Lojinha do Selenium'):
    """Deleta o produto criado nos testes..

    :param product_name: Nome do produto
    :param store_name: Nome da loja que contém o produto.
    """
    conta = Conta.objects.filter(nome=store_name)
    produto = Produto.objects.filter(nome=product_name, conta__in=conta)
    produto.delete()
    del_seo()


def create_shipping_conf(store_name='Lojinha do Selenium',
                         shipping_code='motoboy'):
    """Cria uma configuração de forma de envio.

    :param store_name: O nome da loja de testes que conterá a configuração.
    :param shipping_code: O código da forma de envio.
    """
    envio = Envio.objects.filter(codigo=shipping_code)[0]
    conta = Conta.objects.get(nome=store_name)
    envio_conf = EnvioConfiguracao(conta=conta, forma_envio=envio,
                                   ativo=True)
    envio_conf.save()
    faixa = EnvioFaixaCEP(cep_inicio='00000000', cep_fim='99999999',
                          conta=conta)
    reg = EnvioRegiao(forma_envio=envio, conta=conta, nome='sp')
    reg.save()
    faixa.regiao = reg
    faixa.forma_envio = envio
    faixa.save()
    envio_conf.faixas_cep.add(faixa)
    peso = EnvioFaixaPeso(peso_inicio=0, peso_fim=10000,
                          conta=conta, forma_envio=envio,
                          regiao=reg)
    peso.save()
    envio_conf.faixas_peso.add(peso)
    envio_conf.save()
    return envio_conf


def del_shipping_conf(store_name='Lojinha do Selenium'):
    """Apaga a configuração de envio da loja de testes.

    :param store_name: Nome da loja de testes."""

    contas = Conta.objects.filter(nome=store_name)
    envio_conf = EnvioConfiguracao.objects.filter(conta__in=contas)
    for conf in envio_conf:
        for faixa in conf.faixas_cep.all():
            faixa.delete()

    EnvioRegiao.objects.filter(conta__in=contas).delete()
    envio_conf.delete()


def create_payment_conf(store_name='Lojinha do Selenium',
                        payment_code='entrega'):
    """Cria uma configuração de forma de pagamento.

    :param store_name: Nome da loja de teste.
    :param payment_code: Código da forma de pagamento.
    """

    conta = Conta.objects.get(nome=store_name)
    forma_pagamento = FormaPagamento.objects.get(codigo=payment_code)
    config = FormaPagamentoConfiguracao(conta=conta, ativo=True,
                                        forma_pagamento=forma_pagamento,
                                        json=[1, 2],
                                        eh_padrao=True)
    config.save()
    return config


def del_payment_conf(store_name='Lojinha do Selenium'):
    """Deleta as formas de pagamento da loja de testes.

    :param store_name: O nome da loja de teste."""

    contas = Conta.objects.filter(nome=store_name)
    config = FormaPagamentoConfiguracao.objects.filter(conta__in=contas)
    config.delete()


def _get_model_index_fields(instance):
    """Returns a dict of the model's fields with their values.

    :param instance: An instance of a django model."""

    inst_dict = {}
    for field in instance._meta.fields:
        name = field.name
        value = getattr(instance, name)
        if isinstance(value, Model):
            value = _get_model_index_fields(value)
        elif isinstance(value, UUID):
            value = str(value)

        inst_dict[name] = value

    return inst_dict


def index_products(store_name='Lojinha do Selenium'):
    """Indexa os produtos da loja de teste no elasticsearch

    :param store_name: Nome da loja de teste.."""

    conta = Conta.objects.get(nome=store_name)
    products = Produto.objects.filter(conta=conta)
    index_date = datetime.datetime.now()

    # here we create dicts that will be sent to the elasticsearch
    plist = []
    for product in products:
        pdict = {'@timestamp': index_date,
                 'frete_gratis': False}

        pdict.update(_get_model_index_fields(product))
        pdict['loja'] = pdict['conta']
        pdict['disponivel'] = True
        pdict['categorias'] = []
        pdict['preco'] = {
            'cheio': product.preco.preco_cheio,
            'promocional': product.preco.preco_promocional,
            'venda': product.preco.preco_cheio,
            'sob_consulta': None,
            'com_promocao': None,
            'tem_variacao': False,
        }
        pdict['estoque'] = {
            'gerenciado': False,
            'quantidade': 1,
            'situacao_sem_estoque': 0,
            'situacao_em_estoque': 1,
            'disponivel': True
        }
        pdict['url'] = '/produto/%s.html' % product.apelido
        pdict['produtos_id'] = [product.id]
        del pdict['conta']
        plist.append(pdict)

    es_conn = ElasticsearchConnect(settings.ELASTICSEARCH_ASSISTANCE_URL)
    es_conn.bulk_index('catalogo', 'produto', plist, id_field='id')
    # here we wait for the index process to finish
    time.sleep(1)


def deindex_products(store_name='Lojinha do Selenium'):
    """Remove os produtos de teste do elasticsearch

    :param store_name: O nome da loja de teste."""

    try:
        conta = Conta.objects.get(nome=store_name)
        products = Produto.objects.filter(conta=conta)
        es_conn = ElasticsearchConnect(settings.ELASTICSEARCH_ASSISTANCE_URL)
        for prd in products:
            es_conn.delete('catalogo', 'produto', prd.id)

        time.sleep(1)
    except Conta.DoesNotExist:
        pass


def index_envio(store_name='Lojinha do Selenium'):
    """Indexa as formas de envio do elasticsearch.

    :param store_name: O nome da loja de teste."""


def create_cliente_grupo():
    """Cria um registro de ClienteGrupo para grupo padrão"""

    try:
        cg = ClienteGrupo.grupo_padrao()
    except ClienteGrupo.DoesNotExist:
        cg = ClienteGrupo(nome=u'Padrão')
        cg.save()
    return cg


def del_cliente_grupo():
    """Apaga o grupo de clientes criado para testes"""

    grupos = ClienteGrupo.objects.filter(nome='Padrão', conta_id__isnull=True)
    if grupos.count() > 1:
        for g in grupos[1:]:
            g.delete()


def create_loja(store_name='Lojinha do Selenium'):
    """Cria todas as coisas necessárias para uma loja de teste.

    :param store_name: Um nome para a loja de teste.
    """
    create_user()
    create_conta(store_name=store_name)
    create_plano(store_name=store_name)
    create_product(store_name=store_name)
    create_shipping_conf(store_name=store_name)
    create_payment_conf(store_name=store_name)
    create_cliente_grupo()
    index_products(store_name=store_name)


def del_loja(store_name='Lojinha do Selenium'):
    """Deleta a loja de teste

    :param store_name: Nome da loja de teste.
    """
    del_product()
    del_plano()
    del_shipping_conf()
    del_payment_conf()
    deindex_products()
    del_cliente_grupo()
    del_user()
    del_conta()
