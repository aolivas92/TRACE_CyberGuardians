# mock_http_client.py

class MockHTTPClient:
    @staticmethod
    def fetch_html(url: str) -> str:
        # Simulated HTML for testing purposes
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Crawler Test Page</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="styles.css" rel="stylesheet">
            <script src="script.js"></script>
        </head>
        <body>
            <header>
                <h1>Crawler Test Page</h1>
                <nav>
                    <ul>
                        <li><a href="/nav/page1.html">Navigation 1</a></li>
                <li><a href="/nav/page2.html">Navigation 2</a></li>
                <li><a href="/nav/page3.html">Navigation 3</a></li>
                <li><a href="/nav/page4.html">Navigation 4</a></li>
                <li><a href="/nav/page5.html">Navigation 5</a></li>

                    </ul>
                </nav>
            </header>
            
            <main>
                <section id="links">
                    <h2>Test Links</h2>
                    <ul>
                        <li><a href="/pages/page1.html">Link 1</a></li>
                <li><a href="/pages/page2.html">Link 2</a></li>
                <li><a href="/pages/page3.html">Link 3</a></li>
                <li><a href="/pages/page4.html">Link 4</a></li>
                <li><a href="/pages/page5.html">Link 5</a></li>

                    <li><a href="https://example.com">External Link 1</a></li>
                    <li><a href="https://example.org">External Link 2</a></li>
                    <li><a href="https://test.example.net/path?param=value">External Link with Parameters</a></li>
                    <li><a href="#section">Internal Anchor</a></li>
                    <li><a href="mailto:test@example.com">Email Link</a></li>
                    </ul>
                </section>
                
                <section id="images">
                    <h2>Test Images</h2>
                    <img src="/images/image1.jpg" alt="Test Image 1">
            <img src="/images/image2.jpg" alt="Test Image 2">
            <img src="/images/image3.jpg" alt="Test Image 3">

                </section>
                
                <section id="forms">
                    <h2>Test Forms</h2>
        
                    <form action="/submit/form1" method="post">
                        <label for="username1">Username:</label>
                        <input type="text" id="username1" name="username" required>
                        
                        <label for="password1">Password:</label>
                        <input type="password" id="password1" name="password" required>
                        
                        <button type="submit">Submit Form 1</button>
                    </form>
            
                </section>
            </main>
            
            <footer>
                <p>Footer with <a href="/sitemap.html">Sitemap</a> and <a href="/contact.html">Contact</a></p>
            </footer>
        </body>
        </html>
        """