from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)
    
    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

videoPutArgs = reqparse.RequestParser()
videoPutArgs.add_argument("name", type=str, help="Name of the video is required", required=True)
videoPutArgs.add_argument("views", type=int, help="Views of the video is required", required=True)
videoPutArgs.add_argument("likes", type=int, help="Likes of the video is required", required=True)
    
videoUpdateArgs = reqparse.RequestParser()
videoUpdateArgs.add_argument("name", type=str, help="Name of the video is required")
videoUpdateArgs.add_argument("views", type=int, help="Views of the video is required")
videoUpdateArgs.add_argument("likes", type=int, help="Likes of the video is required")  
    
resourceFields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resourceFields)
    
    def get(self, vidID):
        result = VideoModel.query.filter_by(id=vidID).first()
        if not result:
            abort(404, message="Could not find video with that id")
        return result
    
    @marshal_with(resourceFields)
    def put(self, vidID):
        args = videoPutArgs.parse_args()
        result = VideoModel.query.filter_by(id=vidID).first()
        if result:
            abort(409, message="Video ID taken")
            
        newVid = VideoModel(id=vidID, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(newVid)
        db.session.commit()
        return newVid, 201
    
    @marshal_with(resourceFields)
    def patch(self, vidID):
        args = videoUpdateArgs.parse_args()
        result = VideoModel.query.filter_by(id=vidID).first()
        if not result:
            abort(404, message="Video with ID doesn't exist")
        
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']
            result.likes = args['likes']
            
        db.session.commit()
        
        return result
            
    
    def delete(self, vidID):
        return '', 204
        

api.add_resource(Video, "/video/<int:vidID>")

if __name__ == '__main__':
    app.run(debug=True)