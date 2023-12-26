# model/ForumTopic.py

class ForumTopic:
    def __init__(self, id, title, user_id, created_at):
        self.id = id
        self.title = title
        self.user_id = user_id
        self.created_at = created_at

    # Aquí añadirías métodos para interactuar con la base de datos, como:
    # - Crear un nuevo tema
    # - Obtener todos los temas
    # - Buscar un tema por ID
    # - etc.
