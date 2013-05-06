You can view the running project at www.summalyze.herokuapp.com.
Because of Google's rate limitation, a non-cached search query takes about 3 minutes to run. We have cached the results for 'Harvard', 'Communism', 'Manifold', and 'Biology'.
To submit a query with more than one word, replace spaces with an underscore (e.g. Lebron James -> Lebron_James)

Once you submit a query, you are directed to a page with the links sorted by depth/prereqs. Clicking on a link opens the page in an iframe. You can filter the links by depth using the sliders. The default is for all levels of depth.
Our source code is hosted on github at https://github.com/neelspatel/textbook-generator.git.
You can clone this repository and run our server in localhost (it defaults to listen on port 8000). 

Here are instructions to run the server in localhost from source:
1. Install the following python packages:
	django
	nltk
	BeautifulSoup
	stemming
	
	(We used pip to install the dependencies)

2. Navigate to the code directory and run the command:
	python manage.py runserver

3. Using a web browser, go to localhost:8000





 