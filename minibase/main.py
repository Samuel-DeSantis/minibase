from pprint import pprint
from multiprocessing import Process

from minibase import Minibase
from model import Model
from authorization import Authorization

class Author(Model):
	name: str = 'authors'

	def articles(self):
		return self.has_many(Article, 'author_id')

class Article(Model):
	name: str = 'articles'
	
	def author(self):
		return self.belongs_to(Author, 'author_id')
    
db = Minibase()
auth = Authorization()

Author.connect(db)
Article.connect(db)

Author.create({'name': 'TEXT'})
Article.create({'title': 'TEXT NOT NULL UNIQUE', 'content': 'TEXT', 'author_id': 'INTEGER'})

Author.insert([
    {'name': 'John Doe'},
    {'name': 'Jane Doe'},
    {'name': 'Alice Smith'},
    {'name': 'Bob Johnson'},
    {'name': 'Charlie Brown'}    
])

Article.insert([
	{'title': 'Article 1', 'content': 'Content of article 1', 'author_id': 1},
	{'title': 'Article 2', 'content': 'Content of article 2', 'author_id': 2},
	{'title': 'Article 3', 'content': 'Content of article 3', 'author_id': 1},
	{'title': 'Article 4', 'content': 'Content of article 4', 'author_id': 3},
	{'title': 'Article 5', 'content': 'Content of article 5', 'author_id': 2}
])

article = Article.select(where={'id': 1})[0]
pprint(article)
pprint(article.author())

db.delete('sqlite3')