from flask import jsonify, request
from app import app, db
from models import Post
from datetime import datetime
import logging

@app.route('/api/posts/<int:post_id>/reschedule', methods=['POST'])
def reschedule_post(post_id):
    """API endpoint to reschedule a post via drag and drop"""
    try:
        post = Post.query.get_or_404(post_id)
        data = request.get_json()
        
        # Parse the new scheduled time
        new_time = datetime.fromisoformat(data['scheduled_time'].replace('Z', '+00:00'))
        
        # Update the post
        post.scheduled_time = new_time
        post.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Post rescheduled successfully'})
        
    except Exception as e:
        logging.error(f"Error rescheduling post: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post_api(post_id):
    """Get post details via API"""
    try:
        post = Post.query.get_or_404(post_id)
        return jsonify(post.to_dict())
    except Exception as e:
        logging.error(f"Error fetching post: {e}")
        return jsonify({'error': str(e)}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats_api():
    """Get dashboard statistics via API"""
    try:
        total_posts = Post.query.count()
        scheduled_posts = Post.query.filter_by(status='scheduled').count()
        published_posts = Post.query.filter_by(status='published').count()
        failed_posts = Post.query.filter_by(status='failed').count()
        
        return jsonify({
            'total': total_posts,
            'scheduled': scheduled_posts,
            'published': published_posts,
            'failed': failed_posts
        })
    except Exception as e:
        logging.error(f"Error fetching stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/bulk', methods=['DELETE'])
def bulk_delete_posts():
    """Bulk delete posts"""
    try:
        data = request.get_json()
        post_ids = data.get('post_ids', [])
        
        if not post_ids:
            return jsonify({'error': 'No post IDs provided'}), 400
        
        deleted_count = Post.query.filter(Post.id.in_(post_ids)).delete(synchronize_session='fetch')
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'{deleted_count} posts deleted successfully',
            'deleted_count': deleted_count
        })
        
    except Exception as e:
        logging.error(f"Error bulk deleting posts: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500