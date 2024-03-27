# DNS Resolver
### Скрипты
* Создать окружение - `create-environment.sh`
* Удалить окружение - `deactivate.sh`
* Запустить сервер - `run-server.sh <PORT> <BIND> <EXTERNAL_DNS>`


### Параметры
* `PORT` - по умолчанию 7070
* `BIND` - по умолчанию bind.txt, файл с маппингом доменных имен
* `EXTERNAL_DNS` - по умолчанию 8.8.8.8, куда перенаправлять запрос, если локально не нашелся ответ

### Тестирование
`dig @localhost -p 7070 -t A ya.ru`
