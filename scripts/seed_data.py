"""
Seed database with test data for development
"""
import logging

from sqlmodel import Session, select

from src.auth.models import User
from src.auth.schemas import UserCreate
from src.auth.service import create_user
from src.database import engine
from src.items.models import Item

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_test_users(session: Session, count: int = 5) -> list[User]:
    """Create test users"""
    users = []
    for i in range(count):
        user_in = UserCreate(
            email=f"testuser{i}@example.com",
            username=f"testuser{i}",
            password="testpass123",
            first_name=f"Test{i}",
            last_name="User",
        )
        try:
            user = create_user(session=session, user_create=user_in)
            users.append(user)
            logger.info(f"Created user: {user.email}")
        except Exception as e:
            logger.warning(f"User {user_in.email} already exists or error: {e}")
            # Try to get existing user
            user = session.exec(
                select(User).where(User.email == user_in.email)
            ).first()
            if user:
                users.append(user)
    return users


def create_test_items(session: Session, users: list[User], items_per_user: int = 3):
    """Create test items for users"""
    for user in users:
        for i in range(items_per_user):
            item = Item(
                title=f"Test Item {i+1} for {user.username}",
                description=f"This is a test item description {i+1}",
                owner_id=user.id,
            )
            session.add(item)
            logger.info(f"Created item: {item.title}")
    session.commit()


def main():
    logger.info("Starting database seeding...")
    
    with Session(engine) as session:
        # Create test users
        logger.info("Creating test users...")
        users = create_test_users(session, count=5)
        
        # Create test items
        logger.info("Creating test items...")
        create_test_items(session, users, items_per_user=3)
    
    logger.info("Database seeding completed!")
    logger.info(f"Created {len(users)} users with 3 items each")
    logger.info("Test credentials: testuser0@example.com / testpass123")


if __name__ == "__main__":
    main()

