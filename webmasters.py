#importing libraries
import httplib2,json,codecs
from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

# Credentials
CLIENT_ID = '436768257586-k4sdr6l7piteccrfel13n8a5senrb2nf.apps.googleusercontent.com'
CLIENT_SECRET = 'Rt4rsP-xkeNl13cM9xU2A57N'

# Oauth scope
OAUTH_SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly'

# Redirection for verification code
REDIRECT_URI = 'https://www.odesk.com/'

# Autherising the request with our credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print 'Go to the following link in your browser: ' + authorize_url
code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)
webmasters_service = build('webmasters', 'v3', http=http)

#Getting sitemap information and writing it to an output csv file
site_url='https://www.odesk.com'      
fob=codecs.open('/Users/gudaprudhvihemanth/Desktop/ram.csv','a','utf-8')    
sitemaps = webmasters_service.sitemaps().list(siteUrl=site_url).execute()
if 'sitemap' in sitemaps:
    fob.write("sitemap"+',')
    sitemap_urls = [s['path'] for s in sitemaps['sitemap']]
    fob.write( ",".join(sitemap_urls))
    fob.write('\n'+"sitemap_lastsub"+',')
    sitemap_lastsub = [s['lastSubmitted'] for s in sitemaps['sitemap']]
    fob.write( ",".join(sitemap_lastsub))
    fob.write('\n'+"errors"+',')
    errors = [s['errors'] for s in sitemaps['sitemap']]
    fob.write( ",".join(errors))
    fob.write('\n'+"warnings"+',')
    warnings = [s['warnings'] for s in sitemaps['sitemap']]
    fob.write( ",".join(warnings))
fob.close()    