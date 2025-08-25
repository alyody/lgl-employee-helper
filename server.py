#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

# Change to the directory containing the files
os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = MyHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🚀 LGL Employee Helper is running at http://localhost:{PORT}")
    print("📖 Open your browser and navigate to the URL above")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Automatically open the browser
    try:
        webbrowser.open(f'http://localhost:{PORT}')
    except:
        pass
    
    httpd.serve_forever()