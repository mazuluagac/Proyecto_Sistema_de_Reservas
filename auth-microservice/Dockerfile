FROM php:8.2-fpm

RUN apt-get update && apt-get install -y \
    git unzip libzip-dev libonig-dev libpng-dev libicu-dev zlib1g-dev \
    default-mysql-client \
    && docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath zip intl

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/auth-service

# Copiar TODO el proyecto ANTES de instalar dependencias
COPY . .

# Instalar dependencias
RUN composer install --no-interaction --prefer-dist --optimize-autoloader

# Permisos
RUN chown -R www-data:www-data storage bootstrap/cache \
 && chmod -R 755 storage bootstrap/cache

EXPOSE 8000

CMD ["sh", "-c", "php artisan migrate --force || true && php artisan serve --host=0.0.0.0 --port=8000"]
