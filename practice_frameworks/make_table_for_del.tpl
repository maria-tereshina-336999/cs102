<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
    <h2><center>Мои скрытые заметки</center></h2>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/todo" class="ui  floated small primary button">На главную</a>
                    </th>
                </tr>
            </thead>
            <thead>
                <th>Номер заметки</th>
                <th>Текст</th>
            </thead>
            <tbody>
                %for row in rows:
                  <tr>
                    %for col in row:
                        <td><a href="{{ "http://127.0.0.1:8080/edit/" + str(row[0]) }}">{{ col }}</a></td>
                    %end
                  </tr>
                %end
            </tbody>
        </table>
        </div>
    </body>
</html>