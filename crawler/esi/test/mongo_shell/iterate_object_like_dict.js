/**
 * Created by youzipi on 16/4/20.
 */
db.test.find({}).limit(1).forEach(function (doc) {
    print(doc);
});
