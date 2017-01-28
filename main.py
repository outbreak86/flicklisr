import webapp2
import cgi


# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <link type="text/css" rel="stylesheet" href="serveup/mystyle.css">
    <title>FlickList</title>
</head>
<body>
    <h1>FlickList</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

#Bad movies
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives"
]

#fetch the watchlist
watchlist = [
    "Star Wars",
    "Minions",
    "Freaky Friday",
    "My Favorite Martian"
]

class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """

    def get(self):

        error=self.request.get("error")
        edit_header = "<h3>Edit My Watchlist</h3>"+"<h2>"+cgi.escape(error)+"</h2>"

        # a form for adding new movies
        add_form = """
        <form action="/add" method="post">
            <label>
                I want to add
                <input type="text" name="new-movie"/>
                to my watchlist.
            </label>
            <input type="submit" value="Add It"/>
        </form>
        """

        # TODO 1
        # Include another form so the user can "cross off" a movie from their list.
        remove_form = """
        <form action="/remove" method="post">
            <label>
                I want to remove"""
        remove_form+='<select name = "old-movie">'
        for index, move in enumerate(watchlist):
            remove_form += '<option value="'+move+'">'+move+'</option>'
        remove_form+="""</select>"
                from my watchlist.
            </label>
            <input type="submit" value="Remove It"/>
        </form>
        """

        # TODO 4 (Extra Credit)
        # modify your form to use a dropdown (<select>) instead a
        # text box (<input type="text"/>)


        content = page_header + edit_header + add_form + remove_form + page_footer
        self.response.write(content)


class AddMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/add'
        e.g. www.flicklist.com/add
    """

    def post(self):
        # look inside the request to figure out what the user typed
        new_movie = self.request.get("new-movie")

        #check for errors
        if (not new_movie) or (new_movie.strip() == ""):
            error = "Please specify the movie you want to add."
            self.redirect("/?error=" + cgi.escape(error))

        #Check for bad movies
        if new_movie in terrible_movies:
            error = "Trust me, you don't want to add '{0}' to your Watchlist.".format(new_movie)
            self.redirect("/?error=" + cgi.escape(error, quote=True))
        # build response content
        new_movie = cgi.escape(new_movie)
        new_movie_element = "<strong>" + new_movie + "</strong>"
        watchlist.append(new_movie)
        sentence = new_movie_element + " has been added to your Watchlist!"
        add_form = """
        <form action="/" method="get">
            <input type="submit" value="Home"/>
        </form>
        """
        content = page_header + "<p>" + sentence + "</p>" +add_form+ page_footer
        self.response.write(content)


# TODO 2
# Create a new RequestHandler class called CrossOffMovie, to receive and
# handle the request from your 'cross-off' form. The user should see a message like:
# "Star Wars has been crossed off your watchlist".
class CrossOffMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/remove'
        e.g. www.flicklist.com/remove
    """

    def post(self):
        # look inside the request to figure out what the user typed
        old_movie = self.request.get("old-movie")
        old_movie = cgi.escape(old_movie)
        if old_movie not in watchlist:
            error = "That movie is not in your list."
            self.redirect("/?error=" + cgi.escape(error))
        # build response content
        old_movie_element = "<strike>" + old_movie + "</strike>"
        sentence = old_movie_element + " has been removed from your Watchlist!"
        watchlist.remove(old_movie)
        add_form = """
        <form action="/" method="get">
            <input type="submit" value="Home"/>
        </form>
        """
        content = page_header + "<p>" + sentence + "</p>" +add_form+ page_footer
        self.response.write(content)



# TODO 3
# Include a route for your cross-off handler, by adding another tuple to the list below.
app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', AddMovie),
    ('/remove',CrossOffMovie)
], debug=True)
