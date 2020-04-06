# Fincollect Python test task:
The assignment
Write a REST web service for currency conversion.

Exchange rates might be taken from free sources (e.g. https://openexchangerates.org/) and should be updated once a day. The rates should be stored in a database.

User interface design is not important and up to you.

Currencies:
Czech koruna
Euro
Polish złoty
US dollar.
The application should be tested as well. Code coverage is important.

## Start with Docker
Start app with docker-compose:

`docker-compose up`

Start tests with docker-compose:

`docker-compose -f docker-compose.tests.yml up currency_converter_tests`

Example server: https://converter.alexue4.ru/
