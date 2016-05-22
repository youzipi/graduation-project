/**
 * 0:origin
 * 1:tolower
 * 2:remove stopwords
 * 3:lemma
 */
db.getCollection('AR0').find({}).count();//29609
db.getCollection('AR1').find({}).count();//26409
db.getCollection('AR2').find({}).count();//26285
db.getCollection('AR3').find({}).count();//19987
db.getCollection('AR4').find({}).count();//19480 remove [number|-|=]
db.getCollection('AR5').find({}).count();//19171 remove [number|-|=]

db.getCollection('AR0').find({}).sort({'value': -1}).limit(20);



