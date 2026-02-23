from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

from .services import ChatService
from .db import SessionLocal
from .models import ChatMessage

chat_bp = Blueprint("chat", __name__)
chat_service = ChatService()

@chat_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    message = (data.get("message") or "").strip()
    session_id = (data.get("session_id") or "").strip()

    if not session_id:
        session_id = uuid.uuid4().hex

    if not message:
        return jsonify({"status": "error", "message": "message is required"}), 400

    response = chat_service.handle_message(session_id, message)

    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "response": response
    })

@chat_bp.route("/history", methods=["GET"])
def history():
    session_id = (request.args.get("session_id") or "").strip()
    limit = int(request.args.get("limit") or 50)

    db = SessionLocal()
    try:
        q = db.query(ChatMessage)
        if session_id:
            q = q.filter(ChatMessage.session_id == session_id)

        rows = q.order_by(ChatMessage.created_at.desc()).limit(limit).all()
        rows = list(reversed(rows))

        return jsonify({
            "status": "success",
            "count": len(rows),
            "items": [
                {
                    "id": r.id,
                    "session_id": r.session_id,
                    "role": r.role,
                    "message": r.message,
                    "created_at": r.created_at.isoformat()
                } for r in rows
            ]
        })
    finally:
        db.close()