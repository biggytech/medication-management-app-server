def init_admin_router(prefix, app):
    @app.route(f'/{prefix}/login')
    def login():
        return "Admin - Login"
