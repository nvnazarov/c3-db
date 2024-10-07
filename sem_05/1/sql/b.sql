-- Какие книги (author, title) брал Иван Иванов?

select b.Author, b.Title
from
    Borrowing bw
    join Reader r on r.ID = bw.ReaderNr
    join Book b on b.ISBN = bw.ISBN
where
    r.FirstName = 'Иван' and
    r.LastName = 'Иванов';