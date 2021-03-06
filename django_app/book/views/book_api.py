import requests

from book.models import Book
from config.settings import config

__all__ = (
    'search',
    'search_data'
)


def search_from_google_books(keyword, index=None):
    if index:
        index = index * 10
    else:
        index = 0
    key = config['google']['api_key']
    params = {
        'q': keyword,
        'langRestrict': 'ko',
        'maxResults': 10,
        'startIndex': index,
        'source': keyword,
        'key': key,
    }
    r = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)
    result_dic = r.json()
    return result_dic


def get_isbn_from_google_book(google_id):
    params = {
        'volumeId': google_id
    }
    r = requests.get('https://www.googleapis.com/books/v1/volumes/volumeId', params=params)
    result_dict = r.json()
    identifiers = result_dict['volumeInfo']['industryIdentifiers']
    for identifier in identifiers:
        if identifier['type'] == 'ISBN_13':
            isbn = identifier['identifier']
    return isbn


def get_description_from_google_book(google_id):
    params = {
        'volumeId': google_id
    }
    r = requests.get('https://www.googleapis.com/books/v1/volumes/volumeId', params=params)
    result_dict = r.json()
    google_description = result_dict['volumeInfo']['description']
    if google_description:
        description = google_description
    return description


def search_from_daum_books(keyword):
    apikey = config['daum']['api_key']
    params = {
        'apikey': apikey,
        'output': 'json',
        'q': keyword,
        'searchType': 'isbn',
        'result': 1,
    }
    r = requests.get('https://apis.daum.net/search/book', params=params)
    result_dict = r.json()
    items = result_dict['channel']['item']
    item = items[0]
    return item


def search(keyword, start, end):
    if keyword != '':
        for i in range(end):
            google_result_dic = search_from_google_books(keyword, i)
            google_items = google_result_dic['items']

            for item in google_items:
                google_id = item['id']
                title = item['volumeInfo']['title']

                # authors
                try:
                    authors = item['volumeInfo']['authors'][0]
                except:
                    authors = ''

                # cover_thumbnail
                try:
                    cover_thumbnail = item['volumeInfo']['imageLinks']['thumbnail']
                except:
                    try:
                        isbn = get_isbn_from_google_book(google_id)
                        daum_item = search_from_daum_books(isbn)
                        cover_thumbnail = daum_item['cover_l_url']
                    except:
                        cover_thumbnail = ''

                # publisher
                try:
                    publisher = item['volumeInfo']['publisher']
                except:
                    try:
                        isbn = get_isbn_from_google_book(google_id)
                        daum_item = search_from_daum_books(isbn)
                        publisher = daum_item['pub_nm']
                    except:
                        publisher = ''

                # description
                try:
                    description = item['volumeInfo']['description']
                except:
                    try:
                        google_description = get_description_from_google_book(google_id)
                        description = google_description
                    except:
                        try:
                            isbn = get_isbn_from_google_book(google_id)
                            daum_item = search_from_daum_books(isbn)
                            description = daum_item['description']
                        except:
                            description = ''

                # 데이터베이스에 저장
                defaults = {
                    'title': title,
                    'author': authors,
                    'cover_thumbnail': cover_thumbnail,
                    'publisher': publisher,
                    'description': description,
                    'keyword': keyword,
                }
                Book.objects.update_or_create(
                    google_id=google_id,
                    description='',
                    defaults=defaults
                )


def search_data(keyword, start, end):
    books = []
    if keyword != '':
        for start in range(end):
            google_result_dic = search_from_google_books(keyword, start)
            google_items = google_result_dic['items']

            for item in google_items:
                google_id = item['id']
                title = item['volumeInfo']['title']
                try:
                    authors = item['volumeInfo']['authors'][0]
                except:
                    authors = ''
                try:
                    cover_thumbnail = item['volumeInfo']['imageLinks']['thumbnail']
                    # p = re.compile(r'.*[&]zoom=(\d+).*')
                    # cover_thumbnail = re.sub(p, 2, cover_thumbnail_tmp)
                except:
                    cover_thumbnail = ''
                try:
                    publisher = item['volumeInfo']['publisher']
                except:
                    publisher = ''
                try:
                    description = item['volumeInfo']['description']
                except:
                    description = ''

                item_dict = {
                    'keyword': keyword,
                    'google_id': google_id,
                    'title': title,
                    'author': authors,
                    'cover_thumbnail': cover_thumbnail,
                    'publisher': publisher,
                    'description': description,
                }

                data_exists = Book.objects.filter(google_id=google_id).exists()
                if data_exists != True:
                    books.append(item_dict)

    Book.objects.bulk_create([Book(
        google_id=book['google_id'],
        keyword=book['keyword'],
        title=book['title'],
        author=book['author'],
        cover_thumbnail=book['cover_thumbnail'],
        publisher=book['publisher'],
        description=book['description']
    ) for book in books])


def save_detail_google_book(google_id):
    params = {
        'volumeId': google_id
    }
    r = requests.get('https://www.googleapis.com/books/v1/volumes/volumeId', params=params)
    result_dict = r.json()
    result = result_dict['volumeInfo']

    try:
        publisher = result['publisher']
    except:
        publisher = ''
    # try:
    #     description = result['description']
    # except:
    #     description = ''
    try:
        cover_thumbnail = result['imageLinks']['small']
    except:
        cover_thumbnail = ''

    Book.objects.filter(google_id=google_id).update(
        cover_thumbnail=cover_thumbnail,
        publisher=publisher,
        # description=description
    )
