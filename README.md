## System story

Проект состоит из 3х сервисов:  

- service1 - админка, отвечает за взаимодействие с пользователем, хранение и отображение пользователю информации о введенных функциях и сгенерированных графиках.  
Используется Django, работает на 8000 порту.

- service2 - генератор данных, отвечает за генерацию данных для графика.  
Принимает одну из двух предустановленных функций, генерирует по ним массив [(x, y)].  
Испольуется Flask, timestamp для функций вычисляется на Python, вычисление самих точек в SQL запросе.

- service3 - генератор изображений, генерирует изображение по подготовленным данным.  
Испольуется Flask, формируется запрос на генерацию графика и отправляется в контейнер highcharts-export-node

Для огранизации окружения и взаимодействия сервисов используется docker-compose.
При первом запуске создается три volume (тома):
- postgresql-data - хранилище данных базы данных Postgresql
- redis-data - том для системы кеширования Redis, используется для хранения результатов выполнения задач в Celery,
настроено постоянное хралинище, данные сбрасываются на диск по времени и при выключении контейнера.
- service1-img - хранилище изображений графиков

Данные между service1 и service2, service3 передаются через JSON.

Для работы проекта требуется установленный Docker и docker-compose.

`docker-compose up -d` - Запустить проект  
`docker-compose down` - Остановить  
`docker-compose down -v` - Остановить и удалить тома  

[http://localhost:8000/admin/](http://localhost:8000/admin/) - Админ-панель  
При первом запуске создается пользователь.  
Логин: **admin**  
Пароль: **11122211**  

