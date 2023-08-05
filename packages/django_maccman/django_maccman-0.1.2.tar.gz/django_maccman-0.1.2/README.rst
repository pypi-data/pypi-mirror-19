=======
MAccMan
=======

MAccMan is a reusable django application to facilitate easy management of email accounts, mailboxes, and aliases. **MAccMan is currently under heavy development and not suited for production use.**

Support notes
-------------

Currently mailman is being tested and developed on PostgreSQL only. There are some specific code snippets that assume that PostgreSQL is used as a backend. This will change in the future.

Requirements
------------

- PostgreSQL 9.0 or later with pgcrypto activated for the desired database (tested with 9.5)
- django-cryptofield (available via pip)

Quick start
-----------

1. Make sure you are using PostgreSQL 9.0 or later (tested with 9.5)

2. Add the mailman application to your projects `INSTALLED_APPS` setting like so::

    INSTALLED_APPS = [
        ...,
        'maccman',
    ]

3. Run `./manage.py migrate` to create the required models and views

4. Start the development server and connect to the admin interface. From there you can configure aliases, mailboxes, etc.

5. Configure your postfix and dovecot instances to use the following views:

 - postfix_alias (Contains alias to destination mappings)
 - postfix_domain (Contains all active domains)
 - postfix_mailbox (Contains all active mailboxes
 - dovecot_iterate (Contains all active users)
 - dovecot_password (Contains username to password mappings for all active users)
 - dovecot_user (Contains address to maildir mappings for all active users)

Dovecot
~~~~~~~

MAccMan employs the cryptographic functionalities built into PostgreSQL to secure the users passwords. Therefore, you need to let the databse verify the passwords. To this, you will need the following `WHERE` clause in your dovecot SQL statement::

  WHERE user = '%u' AND password = crypt('%w', password);

This allows the database backend to verify the password and only returns as user when the passwords match. In addition to this `WHERE` clause, you will need to select the following fields::

  ... NULL AS password, 'Y' AS nopassword ...

For more information, please refer to the excellent dovecot documentation

License
-------

MAccMan is published under the terms and coditions of the 3-Clause-BSD-License

