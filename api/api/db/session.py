from sqlalchemy.orm import scoped_session, sessionmaker

SessionLocal = scoped_session(sessionmaker())
