-- Какие книги (ISBN) из категории "Горы" не относятся к категории "Путешествия"?
-- Подкатегории не обязательно принимать во внимание!

select a.ISBN
from BookCat a
where
    a.CategoryName = 'Горы'
    and not exists (
        select 1
        from BookCat b
        where
            a.ISBN = b.ISBN and
            b.CategoryName = 'Путешествия'
    );