import os
from main_folder import app

if __name__ == "__main__":
    app.run_server(debug=True, host=os.getenv("APP_HOST", "127.0.0.1"))
