# -*- coding: utf-8 -*-
import argparse
import datetime
from nltk.corpus import stopwords
from pymongo import MongoClient

parser = argparse.ArgumentParser(description='Mongodb log')
parser.add_argument('--host', metavar='DB Host', type=str, help='the ip for database host')
parser.add_argument('--database', metavar='Collections(SQL:Database)', type=str,
                    help='a name for database(database name for SQL DB)')
parser.add_argument('--collection', metavar='Collection(SQL:Table)', type=str,
                    help='a name for collection (table name for SQL DB)')
parser.add_argument('--key', metavar='Key(SQL:Field)', type=str, help='a key for collection (table field for SQL DB)')
parser.add_argument('--value-array-type', action="store_true", help='set if value is array type')
parser.add_argument('--result', metavar='Collection(SQL:Table)', help='a collection for result')
parser.add_argument('--show-result', action="store_true", help='print the result')
parser.add_argument('--reset-result', action="store_true", help='reset result before job')
parser.add_argument('--delete-result', action="store_true", help='delete result after job done')

if __name__ == "__main__":
    args = parser.parse_args()
    args.host = '127.0.0.1:27017'
    args.database = 'esi'
    args.collection = 'test'
    args.key = 'abstract'
    # args.result = 'AR' + datetime.datetime.now().strftime("tmp_%Y-%m-%d_%H%M%S")
    # args.result = 'AR' + datetime.datetime.now().strftime("_%Y-%m-%d")
    args.result = 'AR2'

    args.show_result = True
    args.reset_result = True

    client = MongoClient(args.host)
    # SQL database
    database = client[args.database]
    # SQL table
    collection = database[args.collection]

    # http://docs.mongodb.org/manual/reference/method/db.collection.mapReduce/
    from bson.code import Code

    mapper = None
    if args.value_array_type:
        mapper = Code(
            """
            function() {
                this.""" + str(args.key) + """.forEach(function(z) {
					(""+z).split(/[\s\[\],\(\)"\.]+/).forEach(function(v) {
						if(v && v.length ){
							v = v.toLowerCase();
							emit(v, 1);
						}
					});
				});
			}
			"""
        )
    else:
        ## todo 用python 替换  1. 单复数合并 2. 全部转为小写
        mapper = """
			function() {
				(""+this.""" + str(args.key) + """).split(/[\s\[\],\(\)"\.]+/).forEach(function(v){
					if(v && v.length ){
				        v = v.toLowerCase();
						emit(v, 1);

					}
				} );
			}
			"""

    reducer = """
		function(key, value) {
			var total = 0;
			for(var i = 0 ; i < value.length ; ++i ) {
				total += value[i];
			}
			return total;

		}
		"""

    if args.reset_result:
        database[args.result].drop()

        # results = collection.map_reduce(mapper, reducer, args.result, full_response=True )
    results = collection.map_reduce(Code(mapper), Code(reducer), args.result, full_response=True)
    print results

    sw = list(stopwords.words('english'))
    other_words = ['The', 'We', 'In', 'This', 'also', 'All', 'using', 'used', 'It', 'However']
    # sw.extend(other_words)
    stopwords = [
        'the',
        'of',
        'and',
        'to',
        'a',
        'in',
        'is',
        'for',
        'that',
        'are',
        'with',
        'The',
        'on',
        'as',
        'by',
        'we',
        'this',
        'an',
        'be',
        'We',
        'from',
        'In',
        'can',
        'which',
        'or'
    ]
    deleted = database[args.result].remove({'_id': {'$in': sw}})

    print "del_count", deleted
    if args.show_result:
        for doc in database[args.result].find().sort('value', -1).limit(20):
            print doc

    if args.delete_result:
        database[args.result].drop()

    client.close()
