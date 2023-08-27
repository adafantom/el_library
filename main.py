def get_shelfs_book(books_count):
    f = open('library.txt', 'w')
    for book in range(books_count):
        shelf_number = input('На какую полку поставить книгу? Ответ: ')
        book_name = input('Название книги: ')
        book_authors = input('Автор книги: ')
        book_format = {
            'name' : str.strip(book_name),
            'authors' : str.strip(book_authors)
        }
        shelf_format = 'Shelf_{} : {} \n'.format(str.strip(shelf_number), book_format)
        f.write(shelf_format)
    f.close()
    print('Книги добавлены')


def read_file_library():
    with open('library.txt', 'r') as f:
        for line in f:
            print(line)


def main():
    books_count = int(input('Сколько книг необходимо добавить? Ответ: '))    
    get_shelfs_book(books_count)
    read_file_library()


if __name__ == '__main__':
    main()
