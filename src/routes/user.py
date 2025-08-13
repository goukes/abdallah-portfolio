from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (admin only in real app)"""
    try:
        current_user_id = get_jwt_identity()
        
        # In a real application, check for admin role
        users = User.query.filter_by(is_active=True).all()
        return jsonify([user.to_public_dict() for user in users])
        
    except Exception as e:
        return jsonify({'error': 'Failed to get users'}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_public(user_id):
    """Get public user information"""
    try:
        user = User.query.filter_by(id=user_id, is_active=True).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_public_dict()})
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user'}), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user (only own profile or admin)"""
    try:
        current_user_id = get_jwt_identity()
        
        # Users can only update their own profile
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name'].strip()
        if 'last_name' in data:
            user.last_name = data['last_name'].strip()
        
        db.session.commit()
        return jsonify({'user': user.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user'}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Deactivate user account"""
    try:
        current_user_id = get_jwt_identity()
        
        # Users can only delete their own account
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.query.get_or_404(user_id)
        user.is_active = False
        
        db.session.commit()
        return jsonify({'message': 'Account deactivated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to deactivate account'}), 500

@user_bp.route('/portfolio/owner', methods=['GET'])
def get_portfolio_owner():
    """Get portfolio owner information (Abdallah Mohammed Elmahdy)"""
    try:
        # Return static portfolio owner information
        portfolio_owner = {
            'name': 'Abdallah Mohammed Elmahdy',
            'title': 'Full Stack Developer',
            'bio': 'Passionate full-stack developer with expertise in modern web technologies, mobile development, and database management.',
            'skills': {
                'frontend': ['JavaScript', 'React.js', 'HTML5', 'CSS3', 'Responsive Design'],
                'backend': ['Node.js', 'Express.js', 'ASP.NET', 'C#'],
                'databases': ['MongoDB', 'MySQL', 'Firebase'],
                'mobile': ['Flutter', 'Mobile Application Development'],
                'programming': ['C++', 'JavaScript', 'C#'],
                'tools': ['Git', 'VS Code', 'Firebase', 'REST APIs']
            },
            'experience': [
                {
                    'title': 'Full Stack Developer',
                    'company': 'Tech Solutions',
                    'period': '2024 - Present',
                    'description': 'Developing modern web applications using React.js, Node.js, and MongoDB.'
                },
                {
                    'title': 'Mobile App Developer',
                    'company': 'Mobile Innovations',
                    'period': '2024 - 2025',
                    'description': 'Created cross-platform mobile applications using Flutter and Firebase.'
                }
            ],
            'education': [
                {
                    'degree': 'Bachelor of Computer Science',
                    'institution': 'University of Technology',
                    'year': '2024',
                    'description': 'Specialized in software engineering and web development.'
                }
            ],
            'contact': {
                'email': 'abdallahmohammedelmhady@gmail.com',
                'phone': '+250 793895937',
                'location': 'Kigali, Rwanda',
                'linkedin': 'https://www.linkedin.com/in/abdallah-mohammed-elmhady-05928b338/',
                'github': 'https://github.com/search?q=iamshaunjp&ref=opensearch&type=repositories'
            }
        }
        
        return jsonify({'portfolio': portfolio_owner}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get portfolio information'}), 500
