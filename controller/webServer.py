from .LibraryController import LibraryController
from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')


library = LibraryController()


@app.before_request
def get_logged_user():
	if '/css' not in request.path and '/js' not in request.path:
		token = request.cookies.get('token')
		time = request.cookies.get('time')
		if token and time:
			request.user = library.get_user_cookies(token, float(time))
			if request.user:
				request.user.token = token


@app.after_request
def add_cookies(response):
	if 'user' in dir(request) and request.user and request.user.token:
		session = request.user.validate_session(request.user.token)
		response.set_cookie('token', session.hash)
		response.set_cookie('time', str(session.time))
	return response


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/catalogue')
def catalogue():
	title = request.values.get("title", "")
	author = request.values.get("author", "")
	page = int(request.values.get("page", 1))
	books, nb_books = library.search_books(title=title, author=author, page=page - 1)
	total_pages = (nb_books // 6) + 1
	return render_template('catalogue.html', books=books, title=title, author=author, current_page=page,
	                       total_pages=total_pages, max=max, min=min)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in dir(request) and request.user and request.user.token:
		return redirect('/')
	email = request.values.get("email", "")
	password = request.values.get("password", "")
	user = library.get_user(email, password)
	if user:
		session = user.new_session()
		resp = redirect("/")
		resp.set_cookie('token', session.hash)
		resp.set_cookie('time', str(session.time))
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = render_template('login.html')
	return resp


@app.route('/logout')
def logout():
	path = request.values.get("path", "/")
	resp = redirect(path)
	resp.delete_cookie('token')
	resp.delete_cookie('time')
	if 'user' in dir(request) and request.user and request.user.token:
		request.user.delete_session(request.user.token)
		request.user = None
	return resp

@app.route('/reserve/book/<int:book_id>')
def reserve_book(book_id):
    # Obtener la información del libro usando 'book_id'
    # Suponemos que existe una función 'get_book_info' que retorna los detalles del libro
    book_info = library.get_book_info(book_id)
    if book_info is None:
        return "Libro no encontrado", 404

    # Renderizar la plantilla de reserva con la información del libro
    return render_template('reserve_book.html', book=book_info)



@app.route('/process_reservation', methods=['POST'])
def process_reservation():
    # Lógica para procesar la reserva
    # Esto incluirá recibir los datos del formulario y almacenar la reserva en la base de datos.
    return "Reserva procesada"  # Esto es solo un marcador de posición y debe ser reemplazado por la lógica real.

@app.route('/forums')
def forums():
    topics = library.list_topics()
    return render_template('forum.html', topics=topics)
@app.route('/forums/<int:topic_id>')
def forum_topic(topic_id):
    topic = library.show_topic(topic_id)
    return render_template('topic.html', topic=topic)
@app.route('/forums/new', methods=['GET', 'POST'])
def new_forum_topic():
    if request.method == 'POST':
        title = request.form['title']
        user_id = request.form['user_id']  # Asegúrate de obtener el ID del usuario correctamente
        library.create_topic(title, user_id)
        return redirect('/forums')
    return render_template('new_topic.html')

@app.route('/forums/<int:topic_id>/reply', methods=['POST'])
def reply_to_topic(topic_id):
    user_id = request.form['user_id']  # Asegúrate de obtener el ID del usuario correctamente
    content = request.form['content']
    library.post_reply(topic_id, user_id, content)
    return redirect(f'/forums/{topic_id}')
