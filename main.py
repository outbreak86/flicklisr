import webapp2
import random

def getRandomMovie():

	# list of movies
	movies = [
		"Sweeney Todd",
		"Toy Story",
		"The Matrix",
		"Ghost Busters",
		"Saw"
	]

	index = random.randint(0,len(movies)-1)

	return movies[index]


class MainHandler(webapp2.RequestHandler):
    def get(self):
    	movieHeader = "<h1>Movie of the day!</h1>"
    	movieparagraph = "<p>"+getRandomMovie()+"</p>"
    	tomorrowHead = "<h1>Tomorrow's movie of the day!</h1>"
    	tomorrowparagraph = "<p>"+getRandomMovie()+"</p>"

    	while movieparagraph == tomorrowparagraph:
    		tomorrowparagraph = "<p>"+getRandomMovie()+"</p>"
    	
        self.response.write(movieHeader+movieparagraph+tomorrowHead+tomorrowparagraph)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
