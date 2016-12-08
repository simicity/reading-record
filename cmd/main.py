import argparse

from article import *
from word import *

#------main------#
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers( dest="tool" )
	
	subparser_article = subparsers.add_parser('article')
	subparser_article.add_argument( "-add", "-a", nargs='+', help="add article", action="store" )
	subparser_article.add_argument( "-show", "-s", nargs='+', help="show list of article", action="store" )
	subparser_article.add_argument( "-find", "-f", nargs='+', help="search article contain word", action="store" )
	subparser_article.add_argument( "-modify", "-m", nargs=2, help="modify article", action="store" )
	subparser_article.add_argument( "-delete", "-d", nargs='+', help="delete article", action="store" )
	subparser_article.add_argument( "-open", "-o", nargs='+', help="open article in safari", action="store" )

	subparser_word = subparsers.add_parser('word')
	subparser_word.add_argument( "-add", "-a", nargs='+', help="add article", action="store" )
	subparser_word.add_argument( "-show", "-s", nargs='+', help="show list of article", action="store" )
	subparser_word.add_argument( "-modify", "-m", nargs=2, help="modify article", action="store" )
	subparser_word.add_argument( "-delete", "-d", nargs='+', help="delete article", action="store" )

	args = parser.parse_args()

	if args.tool == "article":
		if args.add:
			if len( args.add ) == 2:
				addArticle( args.add[0], args.add[1] )
			else:
				addArticle( args.add[0] )
		elif args.show:
			if args.show[0].lower() == "all":
				showArticle()	
			elif args.show[0].lower() == "tag":
				showArticleByTag( args.show )
			else:
				print( 'invalid command' )
		elif args.find:
			findArticleByWord( args.find )
		elif args.modify:
			modifyArticle( args.modify[0], args.modify[1] )	
		elif args.delete:
			deleteArticle( args.delete )
		elif args.open:
			openArticle( args.open )
	elif args.tool == "word":
		if args.add:
			if len( args.add ) == 2:
				addWord( args.add[0], args.add[1] )
			else:
				addWord( args.add[0] )
		elif args.show:
			if args.show[0].lower() == "all":
				showWord()	
			elif args.show[0].lower() == "id":
				showWordByArticle( args.show )
			else:
				print( 'invalid command' )
		elif args.modify:
			modifyWord( args.modify[0], args.modify[1] )	
		elif args.delete:
			deleteWord( args.delete )
