from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name is required')
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and len(phone_number) != 10:
            raise ValueError('Phone number should be exactly ten digits')
        return phone_number

    __table_args__ = (
        UniqueConstraint('name', name='unique_author_name'),
    )

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500))
    category = db.Column(db.String(20), nullable=False)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Title is required')
        if len(title) > 100:
            raise ValueError('Title is too long')
        # if 'clickbait' in title.lower():
        #     raise ValueError('Title contains clickbait')
        # return title
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]

        for phrase in clickbait_phrases:
            if phrase.lower() in title.lower():
                return title

        raise ValueError('Title does not contain clickbait phrases')

        

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content should be at least 250 characters long')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) >= 250:
            raise ValueError('Summary should be a maximum of 250 characters')
        return summary

    

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either Fiction or Non-Fiction.")
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
