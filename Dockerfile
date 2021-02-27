ARG NGINX_VER=1.19.3
FROM nginx:${NGINX_VER}-alpine as build_modsecurity


ARG GEO_DB_RELEASE=2020-10
ARG MODSEC_BRANCH=v3.0.4
ARG OWASP_BRANCH=v3.3/master

WORKDIR /opt

# Install dependencies; includes dependencies required for compile-time options:
# curl, libxml, pcre, and lmdb and Modsec
RUN echo "Installing Dependencies" && \
    apk add --no-cache --virtual general-dependencies \
    fail2ban autoconf automake byacc curl-dev flex g++ gcc git \
    libc-dev libmaxminddb-dev libstdc++ libtool libxml2-dev linux-headers \
    lmdb-dev make openssl-dev pcre-dev yajl-dev zlib-dev && \
    rm -rf /var/cache/apk/*
RUN apk add --no-cache bash less yaml zip \
    php7-fpm php7-json php7-zlib php7-xml php7-pdo php7-phar php7-openssl \
    php7-gd php7-iconv php7-mcrypt php7-session php7-zip \
    php7-curl php7-opcache php7-ctype php7-apcu \
    php7-intl php7-bcmath php7-dom php7-mbstring php7-simplexml php7-xmlreader && \
    rm -rf /var/cache/apk/*
# Clone and compile modsecurity. Binary will be located in /usr/local/modsecurity
RUN echo "Installing ModSec Library" && \
    git clone -b ${MODSEC_BRANCH} --depth 1 https://github.com/SpiderLabs/ModSecurity && \
    git -C /opt/ModSecurity submodule update --init --recursive && \
    (cd "/opt/ModSecurity" && \
        ./build.sh && \
        ./configure --with-lmdb && \
        make && \
        make install \
    ) && \
    rm -fr /opt/ModSecurity \
        /usr/local/modsecurity/lib/libmodsecurity.a \
        /usr/local/modsecurity/lib/libmodsecurity.la

# Clone Modsec Nginx Connector, GeoIP, ModSec OWASP Rules, and download/extract nginx and GeoIP databases
RUN echo 'Cloning Modsec Nginx Connector, GeoIP, ModSec OWASP Rules, and download/extract nginx and GeoIP databases'
RUN git clone -b master --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git
RUN git clone -b ${OWASP_BRANCH} --depth 1 https://github.com/coreruleset/coreruleset.git /usr/local/owasp-modsecurity-crs
RUN wget -O - https://nginx.org/download/nginx-$NGINX_VERSION.tar.gz | tar -xz 
    
# Install ModSecurity and Nginx modules
RUN echo 'Installing Nginx Modules'
RUN cd "/opt/nginx-$NGINX_VERSION" && ./configure --with-compat --add-dynamic-module=../ModSecurity-nginx && make modules && \
    cp /opt/nginx-$NGINX_VERSION/objs/ngx_http_modsecurity_module.so /usr/lib/nginx/modules/ && \
    rm -fr /opt/* && \
    apk del general-dependencies


FROM nginx:${NGINX_VER}-alpine
LABEL maintainer="Jorge Padron <jpadron1986@gmail.com>"
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# Copy nginx, owasp-modsecurity-crs, and modsecurity from the build image
COPY --from=build_modsecurity /etc/nginx/ /etc/nginx/
COPY --from=build_modsecurity /usr/local/modsecurity /usr/local/modsecurity
COPY --from=build_modsecurity /usr/local/owasp-modsecurity-crs /usr/local/owasp-modsecurity-crs
COPY --from=build_modsecurity /usr/lib/nginx/modules/ /usr/lib/nginx/modules/

# Copy local config files into the image
COPY errors /usr/share/nginx/errors
COPY conf/nginx/ /etc/nginx/
COPY conf/modsec/ /etc/nginx/modsec/
COPY conf/owasp/ /usr/local/owasp-modsecurity-crs/

RUN apk add --no-cache \
    curl-dev \
    libmaxminddb-dev \
    libstdc++ \
    libxml2-dev \
    lmdb-dev \
    tzdata \
    yajl && chown -R nginx:nginx /usr/share/nginx
    

WORKDIR /usr/share/nginx/html

EXPOSE 80 443
