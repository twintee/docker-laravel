FROM php:7.4-fpm-buster

ENV ./.bashrc /root

RUN docker-php-ext-install pdo pdo_mysql
# install composer
RUN cd /usr/bin && curl -s http://getcomposer.org/installer | php && ln -s /usr/bin/composer.phar /usr/bin/composer
RUN apt-get update && \
    apt-get install -y \
    git \
    zip \
    unzip \
    vim \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y \
    libpq-dev \
    && docker-php-ext-install pdo_mysql pdo_pgsql \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html