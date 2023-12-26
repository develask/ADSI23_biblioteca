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
		db.execute("INSERT INTO ForumTopic (title, user_id) VALUES (?, ?)", (title, user_id))

	def post_reply(self, topic_id, user_id, content):
		db.execute("INSERT INTO ForumPost (topic_id, user_id, content) VALUES (?, ?, ?)", (topic_id, user_id, content))

	def create_reservation(self, user_id, copy_id, start_date, end_date):
		user = User(user_id)

	def create_reservation(self, user_id, copy_id, start_date, end_date):
		# Here, implement logic to insert a new reservation into the database
		# Ensure that the copy of the book is available for reservation
		# Validate the dates (not exceeding 2 months) and user session
		# Return True if reservation is successful, False otherwise
		return True  # Placeholder for successful reservation

	def get_user_reservations(self, user_id):
		user = User(user_id)
		return user.get_reservations()

	def create_reservation(self, user_id, book_id, start_date, end_date):
		# Aquí iría la lógica para insertar una nueva reserva en la base de datos
		# Debes asegurarte de que la copia del libro esté disponible para reserva
		pass

	def get_user_reservations(self, user_id):
		# Aquí iría la lógica para obtener las reservas realizadas por un usuario
		# Esto incluiría información sobre los libros reservados y las fechas de reserva
		pass