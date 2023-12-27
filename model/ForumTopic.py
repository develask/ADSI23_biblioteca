import sqlite3

class ForumTopic:
    def __init__(self, id, title, user_id, created_at):
        self.id = id
        self.title = title
        self.user_id = user_id
        self.created_at = created_at

    @staticmethod
    def create_new_topic(title, user_id):
        conn = sqlite3.connect('datos.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO ForumTopic (title, user_id) VALUES (?, ?)", (title, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_topic_by_id(topic_id):
        conn = sqlite3.connect('datos.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM ForumTopic WHERE id = ?", (topic_id,))
        topic_data = cur.fetchone()
        conn.close()
        if topic_data:
            return ForumTopic(*topic_data)
        return None

    @staticmethod
    def list_all_topics():
        conn = sqlite3.connect('datos.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM ForumTopic")
        topics_data = cur.fetchall()
        conn.close()
        return [ForumTopic(*topic) for topic in topics_data]
