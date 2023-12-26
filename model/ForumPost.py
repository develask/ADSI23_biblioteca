# model/ForumPost.py

class ForumPost:
    def __init__(self, id, topic_id, user_id, content, created_at):
        self.id = id
        self.topic_id = topic_id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at

    # Aquí puedes añadir métodos para interactuar con la base de datos, tales como:
    # - Crear una nueva respuesta (post)
    # - Obtener todas las respuestas de un tema específico
    # - etc.
