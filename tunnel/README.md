# TCP TUNNEL

### Requirements
Python3 дефолтная библиотека

### Части
(гайд по запуску)
* `python3 -m src.server.main` <PORT> (по умолчанию 9290) - простой TCP сервер, который работает по простому протоколу (конец сообщение обозначается `#STOPAVPCL`)
* `python3 -m src.proxy_server.main` <PORT> (по умолчанию 9291) - прокси TCP сервер, он принимает запросы, может обрабатывать HTTP (в качестве бонуса), но и TCP по умолчанию, конец сообщения (обертка над реальным запросом) `#STOPPROXY`
* `python3 -m src.proxy_agent.main` <SERVER_PORT>, <PROXY_PORT>, <CLIENT_PORT>, <PROXY_CLIENT_PORT> (по умолчанию 9290, 9291, 9292, 9293) - прокси агент, подключается к серверу и ждет на сокете сообщения от него.
* `python3 -m src.user.main` <PROXY_PORT>, <PORT> (по умолчанию 9291, 9295) - простой TCP клиент пользователь, который шлет сообщение по протоколу аналогично простого серверу (в конце сообщения `#STOPAVPCL`).
* `python3 src/http_server/main.py` <PORT> (по умолчанию 9290) - простой HTTP сервер, на любой url может отвечать на `GET` - возвращает простой `HTML`, `POST` - подобие echo, разворачивающего json, посылая `{"key":"some_value"}` в ответ получаем `{"some_value":"key"}`.

### Тестирование
1)  `python3 -m src.server.main` запускаем TCP сервер, запускаем `python3 -m src.proxy_server.main` прокси сервер, `python3 -m src.proxy_agent.main` прокси агент, потом делаем  `python3 -m src.user.main` - простой TCP запрос. В ответ должны увидеть - `This is simple response#STOPAVPCL`. (Порядок запуска важен).
2) `python3 src/http_server/main.py` запускаем HTTP сервер, можно не перезапускать прокси, потом делаем  `curl localhost:9291` должны увидеть HTML. Делаем `curl -X POST --header "Content-Type: application/json" --data '{"key":"value"},{"not_key":"not_value"}' localhost:9290` получаем `{"value":"key"},{"not_value":"not_key"}`.
