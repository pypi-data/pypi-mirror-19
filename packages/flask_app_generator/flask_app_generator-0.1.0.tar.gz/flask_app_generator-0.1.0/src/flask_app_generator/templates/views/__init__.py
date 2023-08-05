import index

BLUEPRINTS = [
    index.blueprint
]


def register_blueprint(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)
