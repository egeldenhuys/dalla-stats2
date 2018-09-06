FROM php:7.0-apache
RUN docker-php-ext-install mysqli
RUN a2enmod remoteip
COPY ./apache2.conf /etc/apache2/apache2.conf
COPY html/ /var/www/html/
EXPOSE 80
