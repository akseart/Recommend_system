import Books
from pyngrok import ngrok
from subprocess import Popen

book = Books.Book.from_csv('data/items.csv')


def main():
    port = 5001
    ngr = None
    flask = None
    try:
        ngr = ngrok.connect(port).public_url
        print(ngr)
        flask = Popen(["waitress-serve", f"--port={port}",
                       "--call", "app:create_app"])
        flask.wait()
    except KeyboardInterrupt:
        pass
    finally:
        if flask:
            flask.kill()
        if ngr:
            ngrok.kill()


if __name__ == '__main__':
    main()
