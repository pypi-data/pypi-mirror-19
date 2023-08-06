jinja2-cli
==========

.. code:: shell

  $ jinja2 helloworld.tmpl data.json --format=json
  $ cat data.json | jinja2 helloworld.tmpl
  $ curl -s http://httpbin.org/ip | jinja2 helloip.tmpl
  $ curl -s http://httpbin.org/ip | jinja2 helloip.tmpl > helloip.html


