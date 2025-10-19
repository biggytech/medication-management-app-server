from flask import Blueprint, request, jsonify

from models.chat_message.operations.create_chat_message import create_chat_message
from models.chat_message.operations.delete_chat_message import delete_chat_message_by_id
from models.chat_message.operations.get_chat_messages import get_chat_messages, get_chat_messages_by_id
from models.chat_message.operations.get_user_conversations import get_user_conversations
from models.chat_message.operations.update_chat_message import update_chat_message, mark_messages_as_read
from models.chat_message.validations import ChatMessageCreate, ChatMessageUpdate
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request, BODY

api_chat_messages = Blueprint('/api/chat-messages', __name__)


@api_chat_messages.route('/conversations', methods=['GET'])
@token_required
def get_conversations(user):
    """Get all conversations for the current user"""
    try:
        conversations = get_user_conversations(user.id)
        return jsonify({
            'success': True,
            'data': conversations
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_chat_messages.route('/conversations/<int:other_user_id>/messages', methods=['GET'])
@token_required
def get_conversation_messages(user, other_user_id):
    """Get messages in a conversation between current user and another user"""
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)

        messages = get_chat_messages(user.id, other_user_id, limit, offset)

        # Mark messages as read when user views the conversation
        mark_messages_as_read(user.id, other_user_id, user.id)

        # Get user names for all messages
        from models.user.operations.get_user_by_id import get_user_by_id
        user_ids = set()
        for message in messages:
            user_ids.add(message.sender_id)
            user_ids.add(message.receiver_id)
        
        users = {}
        for user_id in user_ids:
            user = get_user_by_id(user_id)
            if user:
                users[user_id] = user.full_name
        
        # Format messages with user names
        formatted_messages = []
        for message in messages:
            message_data = message.as_dict()
            message_data['sender_name'] = users.get(message.sender_id)
            message_data['receiver_name'] = users.get(message.receiver_id)
            formatted_messages.append(message_data)
        
        return jsonify({
            'success': True,
            'data': formatted_messages
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_chat_messages.route('/messages', methods=['POST'])
@token_required
def send_message(user):
    """Send a new message"""
    try:
        # Validate request data manually
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Create Pydantic model for validation
        validated_data = ChatMessageCreate(**data)
        
        message = create_chat_message(validated_data, user.id)
        
        # Get user names for the response
        from models.user.operations.get_user_by_id import get_user_by_id
        sender = get_user_by_id(user.id)
        receiver = get_user_by_id(validated_data.receiver_id)
        
        response_data = message.as_dict()
        response_data['sender_name'] = sender.full_name if sender else None
        response_data['receiver_name'] = receiver.full_name if receiver else None
        
        return jsonify({
            'success': True,
            'data': response_data
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_chat_messages.route('/messages/<int:message_id>', methods=['GET'])
@token_required
def get_message(user, message_id):
    """Get a specific message by ID"""
    try:
        message = get_chat_messages_by_id(message_id)
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message not found'
            }), 404

        # Check if user is part of this conversation
        if message.sender_id != user.id and message.receiver_id != user.id:
            return jsonify({
                'success': False,
                'error': 'Access denied'
            }), 403

        # Get user names for the response
        from models.user.operations.get_user_by_id import get_user_by_id
        sender = get_user_by_id(message.sender_id)
        receiver = get_user_by_id(message.receiver_id)
        
        response_data = message.as_dict()
        response_data['sender_name'] = sender.full_name if sender else None
        response_data['receiver_name'] = receiver.full_name if receiver else None
        
        return jsonify({
            'success': True,
            'data': response_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_chat_messages.route('/messages/<int:message_id>', methods=['PUT'])
@token_required
def update_message(user, message_id):
    """Update a message (typically to mark as read)"""
    try:
        # Validate request data manually
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Create Pydantic model for validation
        validated_data = ChatMessageUpdate(**data)
        
        message = get_chat_messages_by_id(message_id)
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message not found'
            }), 404

        # Check if user is part of this conversation
        if message.sender_id != user.id and message.receiver_id != user.id:
            return jsonify({
                'success': False,
                'error': 'Access denied'
            }), 403

        updated_message = update_chat_message(message_id, validated_data)
        
        # Get user names for the response
        from models.user.operations.get_user_by_id import get_user_by_id
        sender = get_user_by_id(updated_message.sender_id)
        receiver = get_user_by_id(updated_message.receiver_id)
        
        response_data = updated_message.as_dict()
        response_data['sender_name'] = sender.full_name if sender else None
        response_data['receiver_name'] = receiver.full_name if receiver else None
        
        return jsonify({
            'success': True,
            'data': response_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_chat_messages.route('/messages/<int:message_id>', methods=['DELETE'])
@token_required
def delete_message(user, message_id):
    """Delete a message"""
    try:
        message = get_chat_messages_by_id(message_id)
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message not found'
            }), 404

        # Only sender can delete their message
        if message.sender_id != user.id:
            return jsonify({
                'success': False,
                'error': 'Access denied'
            }), 403

        success = delete_chat_message_by_id(message_id)
        if success:
            return jsonify({
                'success': True,
                'message': 'Message deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete message'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_chat_messages.route('/conversations/<int:other_user_id>/mark-read', methods=['POST'])
@token_required
def mark_conversation_as_read(user, other_user_id):
    """Mark all messages in a conversation as read"""
    try:
        updated_count = mark_messages_as_read(user.id, other_user_id, user.id)
        return jsonify({
            'success': True,
            'data': {'updated_count': updated_count}
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
