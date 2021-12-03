from flask import Flask, request
from flask import render_template
from flask_paginate import Pagination, get_page_parameter

import configure_and_run


def create_app():
    app = Flask(__name__)

    @app.route('/')
    @app.route('/index')
    def index():
        page = request.args.get(get_page_parameter(), type=int, default=1)

        per_page = 15
        books = configure_and_run.book.get_part(page, per_page)
        pagination = Pagination(page=page,
                                total=len(configure_and_run.book),
                                search=False,
                                record_name='книги',
                                per_page=per_page,
                                display_msg=" "
                                )

        return render_template('index.html',
                               books=books,
                               pagination=pagination,
                               )

    @app.route('/books/<book_id>')
    def createBookPage(book_id):
        try:
            book = configure_and_run.book[int(book_id)]
        except IndexError:
            return "Not found", 404
        recommend = configure_and_run.book.get_recommend(book_id)
        return render_template('books.html', books=book, recomend=recommend)

    return app


if __name__ == '__main__':
    create_app().run()
