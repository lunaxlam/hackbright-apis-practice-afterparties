from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY, 
                'keyword': keyword, 
                'postalCode': postalcode,
                'radius': radius,
                'unit': unit,
                'sort': sort}

    # TODO: Make a request to the Event Search endpoint to search for events
    #
    # - Use form data from the user to populate any search parameters
    
    response = requests.get(url, params=payload)

    # - Make sure to save the JSON data from the response to the `data`
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    #

    data = response.json()
    
    # - Replace the empty list in `events` with the list of events from your
    #   search results

    events = data['_embedded']['events']

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    url = f'https://app.ticketmaster.com/discovery/v2/events/{id}'
    
    payload = {'apikey': API_KEY}
    
    response = requests.get(url, params=payload)

    event = response.json()
    
    venues = event["_embedded"]["venues"]
    
    classifications = event["classifications"]

    return render_template('event-details.html', 
                            event=event, 
                            venues=venues,
                            classifications=classifications)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
