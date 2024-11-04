from webapp.app import app
from webapp.service.vector_service import refresh_vector_index

if __name__ == '__main__':
    refresh_vector_index()
    app.run(debug=True, port=9090)
