from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates( 'name' )
    def validate_name( self, key, name ):
        names = db.session.query( Author.name ).all()
        if not name:
            raise ValueError( "Name must be filled in and > 0 characters." )
        elif name in names:
            raise ValueError( "Name must be unique." )
        return name
    
    @validates( 'phone_number' )
    def validate_phone_number( self, key, phone_number ):
        if not len( phone_number ) == 10:
            raise ValueError( "Phone number must be 10 digits." )
        return phone_number 


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates( 'title' )
    def validate_title( self, key, title ):
        if not title:
            raise ValueError( "Title must be filled in and > 0 characters." )
        required_words = [ "Won't Believe", "Secret", "Top", "Guess" ]
        for word in required_words:
            if word in title:
                return title
        raise ValueError( "Title must contain one of the following words: 'Won't Believe', 'Secret', 'Top', 'Guess'" )
        
    
    @validates( 'content' )
    def validate_content( self, key, content ):
        if len( content ) < 250:
            raise ValueError( "Content must be at least 250 characters." )
        return content
    
    @validates( 'summary' )
    def validate_summary( self, key, summary ):
        if len( summary ) >= 250:
            raise ValueError( "Summary must be shorter than 250 characters." )
        return summary
    
    @validates( 'category' )
    def validate_category( self, key, category ):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError( "Category must be Fiction or Non-Fiction." )
        return category

    @validates( '')

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
