from website import create_app
from flask_cors import CORS

app = create_app()
CORS(app)


if __name__=='__main__':
    app.run('0.0.0.0', port=5001, debug=True)