Создание резервной копии базы данных:

    `docker exec -it coursesmanager_db_1 sh ./usr/local/bin/scripts/backup`


Востановление из резервной копии:
    
    `docker exec -it coursesmanager_db_1 sh ./usr/local/bin/scripts/restore backup.sql.gz`