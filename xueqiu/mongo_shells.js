/**
 * Created by youzipi on 16/6/2.
 */
db.getCollection('stocks').remove({count: 0})

db.getCollection('stocks').updateMany({}, {$set: {count: 0}})


db.comment.createIndex({'symbol': 1}, {background: true, name: '_symbol'})
db.comment.createIndex({id: 1}, {unique: 1, background: true, name: '_xueqiu_id'})