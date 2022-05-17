from bottle import error, redirect, request, route, run, template

from bayes import NaiveBayesClassifier
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/", method="GET")
def add_label():
    s = session()
    label = request.GET.get("label", "")
    id = int(request.GET.get("id", ""))
    row = s.query(News).filter(News.id == id).one()
    row.label = label
    s.add(row)
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    new_news = get_news("https://news.ycombinator.com/newest", n_pages=5)
    s = session()
    for record in new_news:
        if (
            s.query(News)
            .filter(News.title == record["title"] and News.author == record["author"])
            .first()
            is None
        ):
            data = News(
                title=record["title"],
                author=record["author"],
                url=record["url"],
                comments=record["comments"],
                points=record["points"],
                label=None,
            )
            s.add(data)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    classifier = NaiveBayesClassifier()
    X_train = [r.title for r in s.query(News).filter(News.label != None).all()][0:300]
    y_train = [r.label for r in s.query(News).filter(News.label != None).all()][0:300]
    predict_db = s.query(News).filter(News.label == None).all()
    X_predict = [r.title for r in predict_db][0:100]
    classifier.fit(X_train, y_train)
    labels = classifier.predict(X_predict)
    for i in range(30):
        predict_db[i].label = labels[i]
    classified = [x for x in predict_db if x.label == "good"]
    classified.extend([x for x in predict_db if x.label == "maybe"])
    classified.extend([x for x in predict_db if x.label == "never"])
    return template("predictions_template.tpl", rows=classified)


@error(500)
def mistake500(code):
    return (
        "<head>"
        '<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>'
        "</head>"
        "<h2>Ошибка на сервере! </h2>"
        '<th colspan="7">'
        '<a href="/news" class="ui button">Вернуться на главную страницу</a>'
        "</th>"
    )


@error(404)
def mistake404(code):
    return (
        "<head>"
        '<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>'
        "</head>"
        "<h2>Этой страницы не существует!</h2>"
        '<th colspan="7">'
        '<a href="/news" class="ui button">Вернуться на главную страницу</a>'
        "</th>"
    )


if __name__ == "__main__":
    run(host="localhost", port=8080, reloader=True)
