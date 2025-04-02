from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <html>
            <body>
                <a href="/level1/page1">Page 1</a>
                <a href="/level1/page2">Page 2</a>
            </body>
        </html>
    '''

@app.route('/level1/page1')
def page1():
    return '''
        <html>
            <body>
                <a href="/level2/page1">Level 2 - Page 1</a>
            </body>
        </html>
    '''

@app.route('/level1/page2')
def page2():
    return '''
        <html>
            <body>
                <a href="/level2/page2">Level 2 - Page 2</a>
                <a href="/level2/page3">Level 2 - Page 3</a>
            </body>
        </html>
    '''

@app.route('/level2/page1')
@app.route('/level2/page2')
@app.route('/level2/page3')
def final():
    return '<html><body>No more links here.</body></html>'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
