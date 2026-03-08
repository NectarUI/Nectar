class Webview:
    @staticmethod
    def create_webview(url="https://example.com", width=800, height=600):
        return f'<webview src="{url}" style="width:{width}px; height:{height}px;" nodeintegration></webview>'
