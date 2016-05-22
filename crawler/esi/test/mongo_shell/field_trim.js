db.test.find({}, {"keywords": 1}).forEach(function (doc) {
    var cleaned = [];
    doc.research_areas.forEach(function (s) {
        cleaned.push(s.trim())
    });
    print(cleaned);
    db.test.update(
        {"_id": doc._id},
        {"$set": {"research_areas": cleaned}}
    );
});

