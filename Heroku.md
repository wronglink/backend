(on `main`-branch)

1. Install Heroku CLI. [Instruction](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)
2. `heroku login` and register
3. `heroku create`
4. `git push heroku main`
5. `heroku ps:scale web=1`
6. `heroku open` and change to `<url>/admin` and `<url>/v1/users`
7. Create superuser:
```
heroku run python manage.py createsuperuser --email admin@example.com --username admin
```


[Про БД](https://devcenter.heroku.com/articles/getting-started-with-python#provision-a-database)
