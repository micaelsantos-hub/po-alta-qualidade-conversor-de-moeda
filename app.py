"""Ponto de entrada: ``python app.py`` e acesse http://127.0.0.1:5000."""
from conversor.web import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
