from datetime import datetime
from sqlalchemy.sql import func
from .index import db

class PR(db.Model):
    __tablename__ = 'PR'
    pr_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    sourceBranchName = db.Column(db.String, nullable=False)
    targetBranchName = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=True)
    initialFeedback = db.Column(db.Text, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_modified = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f'<PR {self.pr_id}>'

class Conversation(db.Model):
    __tablename__ = 'convo'
    id = db.Column(db.Integer, primary_key=True)
    pr_id = db.Column(db.String, db.ForeignKey('PR.pr_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    role = db.Column(db.String, nullable=False)
    pr = db.relationship('PR', backref=db.backref('convo', lazy=True))

    def __repr__(self):
        return f'<Conversation {self.id} on PR {self.pr_id}>'