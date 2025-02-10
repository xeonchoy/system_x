import asyncio
from flask import Blueprint, jsonify, Response, stream_with_context
from .sync import MessageSync

sync_bp = Blueprint('sync', __name__)

@sync_bp.route('/sync/start', methods=['POST'])
async def start_sync():
    try:
        async with MessageSync() as sync:
            await sync.sync_messages()
            return jsonify({'status': 'success', 'message': 'Sync started'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@sync_bp.route('/sync/stop', methods=['POST'])
async def stop_sync():
    try:
        async with MessageSync() as sync:
            await sync.close()
            return jsonify({'status': 'success', 'message': 'Sync stopped'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@sync_bp.route('/sync/messages')
async def stream_messages():
    async def generate():
        async with MessageSync() as sync:
            while True:
                try:
                    new_messages = await sync.sync_messages()
                    for msg in new_messages:
                        yield f"data: {msg}\n\n"
                    await asyncio.sleep(2)
                except Exception as e:
                    yield f"event: error\ndata: {str(e)}\n\n"
                    break

    return Response(stream_with_context(generate()), mimetype='text/event-stream')
