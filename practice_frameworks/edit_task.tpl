<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
        <form action="/edit/{{no}}" method="get" style="padding: 30px;">
          <input type="text" name="task" value="{{old[0]}}" size="100" maxlength="100">
          <select name="status">
            <option>Сохранить</option>
            <option>Удалить</option>
          </select>
          <br>
          <input type="submit" name="save" value="Сохранить изменения">
        </form>
    </body>
</html>