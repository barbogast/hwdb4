from flask import Flask
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
def hello():
    rows = db_session.query(M.AttrType).all()
    return '<ul>%s</ul>' % '\n'.join(('<li>%s</li>' % r.name for r in rows))


if __name__ == "__main__":
    app.run()