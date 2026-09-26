import os
from flask import Flask , jsonify

from app.config import config_by_name
from app.extensions import db , cors , jwt
from sqlalchemy import inspect , text

def create_app(config_name = None):
    config_name = config_name or os.environ.get("FLASK_ENV" , "development")
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    os.makedirs(os.path.join(app.root_path,".." , 'instance'),exist_ok = True)
    os.makedirs(app.config['UPLOAD_FOLDER'] , exist_ok=True)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )

    from app.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp , url_prefix ="/api/auth")

    with app.app_context():
        from app.models import user, database,model_run , prediction , report
        from app.models.user import Users 
        print("Registered Tables:", db.metadata.tables.keys())

        db.create_all()

        

        admin_username = "skym1618"
        existing_admin = Users.query.filter_by(username=admin_username , role = "ADMIN").first()

        if not existing_admin:
            new_admin = Users(
                username=admin_username,
                email="akashmbytes@gmail.com",
                role= "ADMIN",
            )
            new_admin.set_password("skym1618")
            db.session.add(new_admin)
            db.session.commit()
            print(f"--- Admin user '{admin_username}' successfully seeded! ---")
        else:
            print(f"--- Admin user '{admin_username}' already exists. Skipping seed. ---")


    return app
