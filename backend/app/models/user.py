import uuid
from datetime import datetime, timezone
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(
        db.Enum("admin", "curator", "user", name="user_role"),
        nullable=False,
        default="user",
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    documents = db.relationship(
        "Document", back_populates="uploaded_by_user", lazy="select"
    )
    categories = db.relationship(
        "Category", back_populates="created_by_user", lazy="select"
    )

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
