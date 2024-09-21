from datetime import datetime
from zoneinfo import ZoneInfo
from .index import db

class PR(db.Model):
    __tablename__ = 'PR'
    pr_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)  # Ensure pr_id is unique and a primary key
    title = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    sourceBranchName = db.Column(db.String, nullable=False)
    targetBranchName = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=True)
    initialFeedback = db.Column(db.Text, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(ZoneInfo('Asia/Singapore')))

    def __repr__(self):
        return f'<PR {self.pr_id}>'

class Conversation(db.Model):
    __tablename__ = 'convo'
    id = db.Column(db.Integer, primary_key=True)
    pr_id = db.Column(db.String, db.ForeignKey('PR.pr_id'), nullable=False)  # ForeignKey to PR
    message = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(ZoneInfo('Asia/Singapore')))

    # Relationship to the PR
    pr = db.relationship('PR', backref=db.backref('convo', lazy=True))

    def __repr__(self):
        return f'<Conversation {self.id} on PR {self.pr_id}>'
