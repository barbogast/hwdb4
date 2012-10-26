from flask import Flask, render_template, request
from sqlalchemy.orm import scoped_session, sessionmaker

import model as M


app = Flask(__name__)
app.debug = True
engine = M.get_engine(M.filepath)
Session = M.get_session(engine)
db_session = scoped_session(Session)


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
def index():
    parts = db_session.query(M.Part)
    return render_template('index.html', parts=parts)

@app.route("/part")
def part():
    part = db_session.query(M.Part).filter_by(id=request.args['id']).one()
    return render_template('part.html', part=part)

if __name__ == "__main__":
    app.run()