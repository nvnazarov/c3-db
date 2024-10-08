-- Найдите все прямые рейсы из Москвы в Тверь.
-- (учитывая, что есть транзитивное замыкание)

select c.*
from
    Connection c
    join Station sa on c.fromstation = sa.name
    join Station sb on c.tostation = sb.name
where
    sa.cityname = 'Moscow' and
    sb.cityname = 'Tver';