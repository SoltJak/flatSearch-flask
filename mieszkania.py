from app import app, db
from app.models import User, Flat, Flatcurrent

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Flat': Flat, 'Flatcurrent': Flatcurrent}