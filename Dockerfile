# Use this Dockerfile to build a PostgreSQL image with the students database
FROM postgres:12

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=mysecretpassword
ENV POSTGRES_DB=postgres

# Copy the initialization script to the Docker entrypoint directory
COPY init-db.sh /docker-entrypoint-initdb.d/

EXPOSE 5432