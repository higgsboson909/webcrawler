import unittest
from crawl import get_urls_from_html
from crawl import get_first_paragraph_from_html
from crawl import get_h1_from_html
from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_2(self):
        input_url = "https://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_http(self):
        input_url = "http://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_http_2(self):
        input_url = "http://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_get_h1(self):
        input_html = """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        actual = get_h1_from_html(input_html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)

    def test_get_h1_2(self):
        input_html = """<html>
  <body>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        actual = get_h1_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph(self):
        input_html = """<html>
  <body>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>"""
        actual = get_first_paragraph_from_html(input_html)
        expected = "Learn to code by building real projects."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_2(self):
        input_html = """<html>
  <body>
    <main>
    </main>
  </body>
</html>"""
        actual = get_first_paragraph_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_h1_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
        <p>Outside paragraph.</p>
        <main>
            <p>Main paragraph.</p>
        </main>
    </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_main_with_paragraph(self):
        html = """
        <html><body>
            <main>
                <p>Main paragraph.</p>
                <p>Another one</p>
            </main>
            <p>Outside paragraph</p>
        </body></html>
        """

        actual = get_first_paragraph_from_html(html)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_main_without_paragraph(self):
        html = """
        <html><body>
            <main><div>No p here</div></main>
            <p>Outside paragraph</p>
        </body></html>
        """

        actual = get_first_paragraph_from_html(html)
        expected = "Outside paragraph"
        self.assertEqual(actual, expected)

    def test_no_main_tag(self):
        html = """
        <html><body>
            <p>First outside paragraph</p>
            <p>Second one</p>
        </body></html>
        """
        actual = get_first_paragraph_from_html(html)
        expected = "First outside paragraph"
        self.assertEqual(actual, expected)

    def test_no_paragraphs_anywhere(self):
        html = """
        <html><body>
            <main><div>Nothing here</div></main>
        </body></html>
        """

        actual = get_first_paragraph_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html(self):
        html = """<html>
  <body>
    <a href="https://blog.boot.dev">Go to Boot.dev</a>
    <img src="/logo.png" alt="Boot.dev Logo" />
  </body>
</html>"""
        base_url = "https://blog.boot.dev"
        actual = get_urls_from_html(html, base_url)
        expected = ["https://blog.boot.dev", "https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
