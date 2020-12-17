# http://omz-forums.appspot.com/pythonista/post/5842985077964800

# FontInstaller (by @olemoritz)

# This script installs a custom TTF font on iOS (system-wide).
# It can be used in one of two ways:

# 1. Simply run it in Pythonista, you'll be prompted for the URL of the font 
#    you'd like to install (if there's a URL in the clipboard, it'll be used by default)

# 2. Use it as an 'Open in...' handler, i.e. select this file in Pythonista's 'Open in...
#    menu' setting. This way, you can simply download a ttf file in Safari and open it in
#    Pythonista. The script will then automatically install the downloaded font.

# The script is inspired by the AnyFont app (https://itunes.apple.com/us/app/anyfont/id821560738)
# and the iOS integration of MyFonts (http://meta.myfonts.com/post/80802984786/install-fonts-from-myfonts-on-ios-7-devices)

import plistlib
import BaseHTTPServer
import webbrowser
import uuid
import urllib
import sys
import console
import clipboard
import os

# Request handler for serving the config profile:
class ConfigProfileHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    config = None
    def do_GET(s):
        s.send_response(200)
        s.send_header('Content-Type', 'application/x-apple-aspen-config')
        s.end_headers()
        plist_string = plistlib.writePlistToString(ConfigProfileHandler.config)
        s.wfile.write(plist_string)
    def log_message(self, format, *args):

         pass

def run_server(config):
    ConfigProfileHandler.config = config
    server_address = ('', 0)
    httpd = BaseHTTPServer.HTTPServer(server_address, ConfigProfileHandler)
    sa = httpd.socket.getsockname()
    # Point Safari to the local http server:
    webbrowser.open('safari-http://localhost:' + str(sa[1]))
    # Handle a single request, then stop the server:
    httpd.handle_request()

def main():
    with open('SourceSansPro-Black.ttf', 'r') as f:
            b = f.read()
    with open('SourceSansPro-BlackItalic.ttf', 'r') as f:
            bi = f.read()
    with open('SourceSansPro-Bold.ttf', 'r') as f:
            bo = f.read()
    with open('SourceSansPro-BoldItalic.ttf', 'r') as f:
            boi = f.read()
    with open('SourceSansPro-ExtraLight.ttf', 'r') as f:
            el = f.read()
    with open('SourceSansPro-ExtraLightItalic.ttf', 'r') as f:
            eli = f.read()
    with open('SourceSansPro-Italic.ttf', 'r') as f:
            i = f.read()
    with open('SourceSansPro-Light.ttf', 'r') as f:
            l = f.read()
    with open('SourceSansPro-LightItalic.ttf', 'r') as f:
            li = f.read()
    with open('SourceSansPro-Regular.ttf', 'r') as f:
            r = f.read()
    with open('SourceSansPro-Semibold.ttf', 'r') as f:
            sb = f.read()
    with open('SourceSansPro-SemiboldItalic.ttf', 'r') as f:
            sbi = f.read()

    # Create the configuration profile:
    unique_id = uuid.uuid4().urn[9:].upper()
    config = {'PayloadContent': [{
              'Font': plistlib.Data(b),
              'PayloadIdentifier': 'org.adobe.font.' + unique_id, 
              'PayloadOrganization': 'Adobe',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': unique_id, 'PayloadVersion': 1},
              {'Font': plistlib.Data(bi),
               'PayloadIdentifier': 'org.adobe.font.' + '123', 
              'PayloadOrganization': 'Adobe',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '654', 'PayloadVersion': 1},
              {'Font': plistlib.Data(bo),
               'PayloadIdentifier': 'org.adobe.font.' + '456', 
              'PayloadOrganization': 'Adobe',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '987', 'PayloadVersion': 1},
              {'Font': plistlib.Data(boi),
               'PayloadIdentifier': 'org.adobe.font.' + '789', 
              'PayloadOrganization': 'Adobe',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '1000', 'PayloadVersion': 1},
              {'Font': plistlib.Data(el),
               'PayloadIdentifier': 'org.adobe.font.' + '1234', 
              'PayloadOrganization': 'Adobe',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '8765', 'PayloadVersion': 1},
              {'Font': plistlib.Data(eli),
               'PayloadIdentifier': 'org.adobe.font.' + '5678', 
              'PayloadOrganization': 'Adobe',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '9012', 'PayloadVersion': 1},
              {'Font': plistlib.Data(i),
               'PayloadIdentifier': 'org.adobe.font.' + '12345', 
              'PayloadOrganization': 'Adobe',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '98765', 'PayloadVersion': 1},
              {'Font': plistlib.Data(l),
               'PayloadIdentifier': 'org.adobe.font.' + '67890', 
              'PayloadOrganization': 'Adobe',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '54321', 'PayloadVersion': 1},
              {'Font': plistlib.Data(li),
               'PayloadIdentifier': 'org.adobe.font.' + '123456', 
              'PayloadOrganization': 'Adobe',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '987654', 'PayloadVersion': 1},
              {'Font': plistlib.Data(r),
              'PayloadIdentifier': 'org.adobe.font.' + '234567', 
              'PayloadOrganization': 'Adobe',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '1890', 'PayloadVersion': 1},
              {'Font': plistlib.Data(sb),
               'PayloadIdentifier': 'org.adobe.font.' + '345678', 
              'PayloadOrganization': 'Adobe',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '1290', 'PayloadVersion': 1},
              {'Font': plistlib.Data(sbi),
               'PayloadIdentifier': 'org.adobe.font.' + '456789', 
              'PayloadOrganization': 'Adobe',
              'PayloadType': 'com.apple.font',
              'PayloadUUID': '1230', 'PayloadVersion': 1},
              ], 
            'PayloadDescription': 'Adobe Source Sans Pro',
            'PayloadDisplayName': 'Adobe Source Sans Pro',
            'PayloadIdentifier': 'org.adobe.font.' + unique_id,
            'PayloadOrganization': 'Adobe', 
            'PayloadRemovalDisallowed': False, 
            'PayloadType': 'Configuration',
            'PayloadUUID': unique_id,
            'PayloadVersion': 1}
    run_server(config)

if __name__ ==  '__main__':
    main()

# def font_dict(filename, payload_id=None, payload_uuid=None):
#    payload_id = payload_id or uuid.uuid4().urn[9:].upper()
#    payload_uuid = payload_uuid or payload_id
#    with open(filename) as in_file:
#        font_data = in_file.read()
#    return { 'Font': plistlib.Data(font_data),
#              'PayloadIdentifier': 'org.scj643.font.{}'.format(payload_id)
#              'PayloadOrganization': 'scj643',
#              'PayloadType': 'com.apple.font',
#              'PayloadUUID': payload_uuid,
#              'PayloadVersion': 1 }

#     config = {'PayloadContent': [font_dict('Ubuntu-{}.ttf'.format(x))
#                                 for x in 'R RI B BI C L LI M MI'.split()]
#               ...
