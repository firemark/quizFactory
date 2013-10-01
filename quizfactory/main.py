from quizfactory import app
import conf

if __name__ == '__main__':

    print("Loading views...")
    for name in conf.urls.keys():
        __import__("views.%s" % name)
    print("Done.")
    app.debug = True
    app.run()