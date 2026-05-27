from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name)

    celery.conf.update(
        broker_url=app.config['broker_url'],
        result_backend=app.config['result_backend']
    )

    return celery