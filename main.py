import views
from app import app, scheduler
from models import Service, Setting

app.register_blueprint(views.blueprint)


def create_table():
    Service.create_table()
    Setting.create_table()


if __name__ == '__main__':
    create_table()
    scheduler.start()
    app.run()
