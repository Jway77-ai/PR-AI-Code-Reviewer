from datetime import datetime
from zoneinfo import ZoneInfo
from .index import db

# Helper function to convert datetime to GMT+8
def current_time_gmt8():
    return datetime.now(ZoneInfo('Asia/Singapore'))

class PR(db.Model):
    __tablename__ = 'PR'
    pr_id = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    sourceBranchName = db.Column(db.String(255), nullable=False)
    targetBranchName = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    initialFeedback = db.Column(db.Text, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=current_time_gmt8)  

    def __repr__(self):
        return f'<PR {self.pr_id}>'

class Conversation(db.Model):
    __tablename__ = 'convo'
    id = db.Column(db.Integer, primary_key=True)
    pr_id = db.Column(db.String(255), db.ForeignKey('PR.pr_id'), nullable=False)  
    message = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=current_time_gmt8)  
    role = db.Column(db.String(50), nullable=False)
    # Relationship to the PR
    pr = db.relationship('PR', backref=db.backref('convo', lazy=True))

    def __repr__(self):
        return f'<Conversation {self.id} on PR {self.pr_id}>'
