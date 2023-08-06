Labirinto Flask
===============
.. image:: https://travis-ci.org/gilzoide/labirinto-flask.svg?branch=master
    :target: https://travis-ci.org/gilzoide/labirinto-flask

Joguinho de labirinto, feito em web usando Flask como servidor, e GTM para tags.

Isso é só um teste das tecnologias.

Divirta-se ;]


Para rodar
----------
Instale as dependências (opcionalmente usando um virtualenv_)::

    $ pip install -r requirements.txt

E rode: ::

    $ python run.py


Para rodar testes de unidade
----------------------------
Instale as dependências (opcionalmente usando um virtualenv_)::

    $ pip install -r test-requirements.txt

E rode: ::

    $ nosetests


Docker
------
Há configuração para criar um container do Docker_ prontim pra rodar os bang.
Para criar a imagem, opcionalmente instalando os pacotes de teste automatizado::

    $ docker build -t <NomeDaImagem> [--build-arg TESTE=true] docker/

Para rodar o programa, ou os testes, substitua `OPTIONS` pelas opções do
`docker run`_ e `COMANDO` por um
dos comandos citados acima::

    $ docker run OPTIONS <MesmoNomeDaImagem> /sbin/my_init -- COMANDO


.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _Docker: https://www.docker.com/
.. _docker run: https://docs.docker.com/engine/reference/run/
