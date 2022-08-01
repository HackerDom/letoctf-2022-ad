SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@postgres/postgres'
SECRET_KEY = open('/var/data/secret_key', 'rb').read()