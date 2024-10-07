-- Какие читатели (LastName, FirstName) вернули копию книги?

select r.LastName, r.FirstName
from
    Borrowing bw
    join Reader r on r.ID = bw.ReaderNr
where bw.ReturnDate < CURRENT_DATE;