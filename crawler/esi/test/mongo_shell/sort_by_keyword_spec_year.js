var top_20_keywords = db.getCollection('test').aggregate(
//     {'$unwind': '$cleaned_research_areas'}
    {'$unwind': '$cleaned_keywords'}
//     , {
//         $match: {
//             pub_year: 201
//         }
//     }
    , {
        $group: {
            _id: {'keywords': '$cleaned_keywords'},
//             _id: {'keywords': '$cleaned_research_areas'},
            paper_count: {$sum: 1},
            per_citations: {$avg: '$citations'},
//         papers:{$addToSet:'$title'}
        }
    }
    , {$sort: {paper_count: -1}}
//     ,{$limit:20}

);
top_20_keywords.forEach(function (d) {
//     printjson(d);
    print(d._id.keywords,d.paper_count,d.per_citations);
});

