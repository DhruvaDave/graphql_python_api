from api import create_app
from utils.db_handler import register_models


register_models()
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4500, debug=False)