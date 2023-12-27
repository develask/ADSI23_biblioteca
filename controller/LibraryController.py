from model import Connection, Book, User, ForumTopic, ForumPost
from model.tools import hash_password

db = Connection()

class LibraryController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(LibraryController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance


	def search_books(self, title="", author="", limit=6, page=0):
		count = db.select("""
				SELECT count() 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
		""", (f"%{title}%", f"%{author}%"))[0][0]
		res = db.select("""
				SELECT b.* 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{title}%", f"%{author}%", limit, limit*page))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in res
		]
		return books, count

	def get_user(self, email, password):
		user = db.select("SELECT * from User WHERE email = ? AND password = ?", (email, hash_password(password)))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2])
		else:
			return None

	def get_user_cookies(self, token, time):
		user = db.select("SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?", (time, token))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2])
		else:
			return None

	def get_book_info(self, book_id):
		# Realizar una consulta a la base de datos para obtener la información del libro
		res = db.select("SELECT * FROM Book WHERE id = ?", (book_id,))
		if len(res) > 0:
			# Convertir el resultado en un objeto 'Book'
			return Book(res[0][0], res[0][1], res[0][2], res[0][3], res[0][4])
		else:
			return None

	def list_topics(self):
		res = db.select("SELECT * FROM ForumTopic")
		topics = [ForumTopic(t[0], t[1], t[2], t[3]) for t in res]
		return topics

	def show_topic(self, topic_id):
		topic_res = db.select("SELECT * FROM ForumTopic WHERE id = ?", (topic_id,))
		topic = None
		if topic_res:
			t = topic_res[0]
			topic = ForumTopic(t[0], t[1], t[2], t[3])

		replies_res = db.select("SELECT * FROM ForumPost WHERE topic_id = ?", (topic_id,))
		replies = [ForumPost(p[0], p[1], p[2], p[3], p[4]) for p in replies_res]

		return topic, replies

	def create_topic(self, title, user_id):
		# Suponiendo que 'db' es tu objeto de conexión a la base de datos
		cursor = db.cursor()  # Obtener un cursor
		cursor.execute("INSERT INTO ForumTopic (title, user_id) VALUES (?, ?)", (title, user_id))
		db.commit()  # Guardar los cambios
		cursor.close()  # Cerrar el cursor
	def post_reply(self, topic_id, user_id, content):
		db.execute("INSERT INTO ForumPost (topic_id, user_id, content) VALUES (?, ?, ?)", (topic_id, user_id, content))