""" The Book Application """
import traceback

from bookdb import BookDB

DB = BookDB()


def book(book_id):
    """ Function to return details of a book """
    try:
        details = DB.title_info(book_id)
        msg = "<H1>Title: {}</H1>".format(details['title'])
        msg += "<H4>ISBN: {}</H4>".format(details['isbn'])
        msg += "<H4>Publisher: {}</H4>".format(details['publisher'])
        msg += "<H4>Author: {}</H4>".format(details['author'])
        msg += "<br><H6><a href='/'>Back</a></H6>"
        return msg
    except TypeError:
        raise NameError


def books():
    """ Function to return all the books """
    msg = "<h1>My Library</h1>"
    for title in DB.titles():
        msg += "<h4>{}:  <a href='book/{}'>{}</a></h4>".format(title['id'],
                                                               title['id'],
                                                               title['title'])

    return msg


def resolve_path(path):
    """ Function path resolution from URI """
    funcs = {
        '': books,
        'book': book
        }

    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    """ The application routing and execution """
    status = "200 OK"
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)

        if path is None:
            raise NameError

        func, args = resolve_path(path)
        body = func(*args)
        status = '200 OK'
    except NameError:
        body = '<h1>404 Not Found</h1>'
        status = '404 Not Found'
    except Exception:
        body = '<h1>500 Server Error</h1'
        status = '500 Server Error'
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    SRV = make_server('localhost', 8080, application)
    SRV.serve_forever()
