zato-apitest is a friendly command line tool for creating beautiful tests of HTTP-based REST, XML and SOAP APIs with as little
hassle as possible.

Tests are written in plain English, with no programming needed, and can be trivially easy extended in Python if need be.

Note that zato-apitest is meant to test APIs only. It's doesn't simulate a browser nor any sort of user interactions. It's meant
purely for machine-machine API testing.

Originally part of `Zato <https://zato.io>`_ - open-source ESB, SOA, REST, APIs and cloud integrations in Python.

In addition to HTTP Zato itself supports AMQP, ZeroMQ, WebSphere MQ, including JMS, Redis, FTP, OpenERP, SMTP, IMAP, SQL, Amazon S3,
OpenStack Swift and more so it's guaranteed zato-apitest will grow support for more protocols and transport layers with time.

Here's a sample test case::

    Feature: Customer update

    Scenario: SOAP customer update

        Given address "http://example.com"
        Given URL path "/xml/customer"
        Given SOAP action "update:cust"
        Given HTTP method "POST"
        Given format "XML"
        Given namespace prefix "cust" of "http://example.com/cust"
        Given request "cust-update.xml"
        Given XPath "//cust:name" in request is "Maria"
        Given XPath "//cust:last-seen" in request is a random date before "2015-03-17" "default"

        When the URL is invoked

        Then XPath "//cust:action/cust:code" is an integer "0"
        And XPath "//cust:action/cust:msg" is "Ok, updated"

        And context is cleaned up

    Scenario: REST customer update

        Given address "http://example.com"
        Given URL path "/json/customer"
        Given query string "?id=123"
        Given HTTP method "PUT"
        Given format "JSON"
        Given header "X-Node" "server-test-19"
        Given request "cust-update.json"
        Given JSON Pointer "/name" in request is "Maria"
        Given JSON Pointer "/last-seen" in request is UTC now "default"

        When the URL is invoked

        Then JSON Pointer "/action/code" is an integer "0"
        And JSON Pointer "/action/message" is "Ok, updated"
        And status is "200"
        And header "X-My-Header" is "Cool"

More details, including plenty of usage examples, demos and screenshots, are `on GitHub <https://github.com/zatosource/zato-apitest>`_.


