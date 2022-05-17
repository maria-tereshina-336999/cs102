<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
    <h2><center>Предсказанное ранжирование новостей</center></h2>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/news" class="ui  floated small primary button">На главную страницу</a>
                    </th>
                </tr>
            </thead>
            <thead>
                <th>Название</th>
                <th>Автор</th>
                <th>Лайки</th>
                <th>Комментарии</th>
                <th colspan="3">Метки</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr>
                    <td><a href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                    % if row.label == "good":
                        <td class="positive">Интересно</td>
                    % elif row.label == "maybe":
                        <td class="active">Возможно прочитаю</td>
                    % elif row.label == "never":
                        <td class="negative">Не интересно</td>
                    % else:
                        <td>{{row.label}}</td>
                    % end
                </tr>
                %end
            </tbody>
        </table>
        </div>
    </body>
</html>