Hydra is a tool for visualizing org charts and org chart meta data (locations, legal entities, departments, divisions, etc). 

At present this is a no-frills implementation without a test suite or sample data set!

It is written in Python for the back end (Flask) and Javascript on the front end (visjs).

At present Hydra just supports reading in a csv file and serving up a web page with a select box for the columns of the csv file (the "dimensions") and a dim with the visjs graph inside of it.

