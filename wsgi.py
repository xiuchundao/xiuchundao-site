from app import create_app

application = create_app('product')

if __name__ == '__main__':
    application.run()
