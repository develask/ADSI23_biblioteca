import sqlite3


class ForumPost:
    def __init__(self, id, topic_id, user_id, content, created_at):
        self.id = id
        self.topic_id = topic_id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at

    @staticmethod
    def post_reply(topic_id, user_id, content):
        conn = sqlite3.connect('datos.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO ForumPost (topic_id, user_id, content) VALUES (?, ?, ?)", (topic_id, user_id, content))
        conn.commit()
        conn.close()

    @staticmethod
    def get_replies_by_topic(topic_id):
        conn = sqlite3.connect('datos.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM ForumPost WHERE topic_id = ?", (topic_id,))
        replies_data = cur.fetchall()
        conn.close()
        return [ForumPost(*reply) for reply in replies_data]
