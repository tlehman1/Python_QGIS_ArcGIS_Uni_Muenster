from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView

# create new empty WebView
newWebView = QWebView(None)

# Loading the URL into the created WebView
newWebView.load(QUrl('https://wikipedia.org/wiki/[%name%]'))

# Display webview in a pop up window
newWebView.show()