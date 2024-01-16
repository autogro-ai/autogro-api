FROM mysql:latest
ENV MYSQL_DATABASE=db
ENV MYSQL_ROOT_PASSWORD=password1234
COPY ./sql_scripts/* /docker-entrypoint-initdb.d/
EXPOSE 3306
