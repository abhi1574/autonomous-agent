import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.models.database import SessionLocal, engine
from backend.models.user import User, UserRole
from backend.models import task
from backend.models.database import Base
from passlib.context import CryptContext

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

existing = db.query(User).filter(User.username == "admin").first()
if not existing:
    admin = User(
        username        = "admin",
        email           = "admin@agent.local",
        hashed_password = pwd_context.hash("admin123"),
        role            = UserRole.admin 
    )
    db.add(admin)
    db.commit()
    print("✅ Admin user created — username: admin, password: admin123")
else:
    print("⚠️  Admin user already exists")

db.close()