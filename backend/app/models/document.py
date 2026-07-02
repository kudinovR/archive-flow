import uuid
from datetime import datetime, timezone
from app.extensions import db


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(512), nullable=False)
    status = db.Column(
        db.Enum("pending", "approved", "rejected", name="document_status"),
        nullable=False,
        default="pending",
    )
    rejection_reason = db.Column(db.Text, nullable=True)
    uploaded_by = db.Column(
        db.UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False
    )
    category_id = db.Column(
        db.UUID(as_uuid=True), db.ForeignKey("categories.id"), nullable=True
    )
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    uploaded_by_user = db.relationship(
        "User", back_populates="documents", lazy="select"
    )
    category = db.relationship("Category", back_populates="documents", lazy="select")

    def __repr__(self):
        return f"<Document {self.filename} ({self.status})>"
