# transaction_control
Тестовое задание


Нужно реализовать систему транзакций. 

**Как происходит транзакция:**

Идет запрос на сервер от клиента, по клиенту выстраивается очередь на вывод.
Важно: 
1) у каждого клиента есть своя очередь; 
2) при нехватке денег, нужно блокировать запрос.

**Что нужно реализовать:**

бд на postgresql, где будет схема с клиентами и их балансами
сервер, которые проверяет все условия(хватает ли денег, если сервер упадет, то история, которая идет на вывод не должна пропасть) и делает изменение баланса(на + или -)