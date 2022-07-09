import os
from travel_api_setup import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(port=port, debug=True)
