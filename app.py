from .__init__ import create_app, socketio

app = create_app()

if __name__ == "__main__":
    # set FLASK_APP=app.py
    # flask run
    # app = create_app()
    socketio.run(app, debug=True)