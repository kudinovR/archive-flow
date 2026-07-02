import uuid
from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(
        db.UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False
    )

    created_by_user = db.relationship(
        "User", back_populates="categories", lazy="select"
    )
    documents = db.relationship("Document", back_populates="category", lazy="select")

    def __repr__(self):
        return f"<Category {self.name}>"
