-- Какие читатели (LastName, FirstName) брали хотя бы одну книгу (не копию),
-- которую брал также Иван Иванов (не включайте Ивана Иванова в результат)?

with IvanIvanovBooks as (
    select ISBN
    from Borrowing
    where ReaderNr = (
        select ID
        from Reader
        where
            FirstName = 'Иван' and
            LastName = 'Иванов'
    )
)
select r.LastName, r.FirstName
from
    Reader r
    join Borrowing bw on r.ID = bw.ReaderNr
    join IvanIvanovBooks iib on iib.ISBN = bw.ISBN
where
    not (r.FirstName = 'Иван' and r.LastName = 'Иванов');