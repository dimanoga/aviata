# aviata
Для запуска сервиса вне докера нужно запустить сервер postresql и redis. Затем в терминал написать make pre-init
для установки нужных библиотек, затем make init для создания бд.

## Для запуска в докере
    docker-compose build
    docker-compose up