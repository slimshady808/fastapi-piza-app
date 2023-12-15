from piza_api.database import engine,Base
from piza_api.models import User,Order

Base.metadata.create_all(bind=engine)