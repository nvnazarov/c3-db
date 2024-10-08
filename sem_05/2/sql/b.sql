-- Найдите все многосегментные маршруты, имеющие точно однодневный
-- трансфер из Москвы в Санкт-Петербург (первое отправление и прибытие
-- в конечную точку должны быть в одну и ту же дату).
-- Вы можете применить функцию DAY () к атрибутам Departure и Arrival, чтобы определить дату.

select c.*
from
    connection c
    join Station sa on c.fromstation = sa.name
    join Station sb on c.tostation = sb.name
where
    sa.cityname = 'Moscow' and
    sb.cityname = 'St.Petersburg' and
    extract(day from c.departure) = extract(day from c.arrival);