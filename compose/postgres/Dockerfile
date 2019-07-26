FROM postgres:11.4-alpine

COPY ./compose/postgres/backup /usr/local/bin/scripts/backup
RUN chmod +x /usr/local/bin/scripts/backup

COPY ./compose/postgres/restore /usr/local/bin/scripts/restore
RUN chmod +x /usr/local/bin/scripts/restore