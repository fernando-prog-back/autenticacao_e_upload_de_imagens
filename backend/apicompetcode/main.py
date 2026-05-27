from competcode import app

if __name__ == '__main__':
    app.run(debug=True)


# Antes tem que rodar o celery: celery -A judge.judge worker --loglevel=info -P threads --concurrency=10 