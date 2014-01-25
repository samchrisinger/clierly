import views

def init(app):
    @app.route('/', methods=['GET'])
    def index():
        return views.index(request)

    @app.route('/parser', methods=['POST'])
    def parse():
        return views.process(request)
    
