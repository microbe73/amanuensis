from sqlalchemy import func

from amanuensis.errors import NotFound, UserError
from amanuensis.models import (
    Message,
)


__all__ = [
    "get_all_messages",
    "get_messages_by_request",
    "send_message",
]


def get_all_messages(current_session, logged_user_id):
    messages = current_session.query(Message).filter_by(sender_id=logged_user_id).all()
    return messages


def get_messages_by_request(current_session, logged_user_id, request_id):
    # messages = current_session.query(Message).filter(Message.sender_id == logged_user_id, Message.request_id == request_id).all()
    messages = current_session.query(Message).filter(Message.request_id == request_id).all()
    return messages


def send_message(current_session, logged_user_id, request_id, body, receivers):
    new_message = Message(sender_id=logged_user_id, 
                        body=body,
                        request_id=request_id)
    
    current_session.add(new_message)
    new_message.receivers.extend(receivers)
    current_session.commit()
    return new_message