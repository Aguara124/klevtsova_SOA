# API Gateway Service

Данный сервис необходим для маршрутизации запросов через REST API.  
Получив запрос от пользователя, сервис перенаправляет его в один из трех сервисов. Соответственно, его зона ответственности: получать http запросы и маршрутизировать их, границы - маршруты через определенные api к другим микросервисам. 
