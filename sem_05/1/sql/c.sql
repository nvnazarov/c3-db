-- Какие книги (ISBN) из категории "Горы" не относятся к категории "Путешествия"?
-- Подкатегории не обязательно принимать во внимание!

select ISBN
from BookCat
where
    CategoryName = 'Горы'
    and (ISBN, 'Путешествия') not in BookCat;