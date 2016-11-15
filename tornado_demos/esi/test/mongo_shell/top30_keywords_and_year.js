var top_30_keywords = db.getCollection('test').aggregate(
//     {'$unwind': '$cleaned_research_areas'}
    {'$unwind': '$cleaned_keywords'}
    , {
        $match: {
            pub_year: {$in:[2013,2014,2015]}
        }
    }
    , {
        $group: {
            _id: {'keywords': '$cleaned_keywords'},
//             _id: {'keywords': '$cleaned_research_areas'},
            paper_count: {$sum: 1},
//             per_citations: {$avg: '$citations'},
//         papers:{$addToSet:'$title'}
        }
    }
    , {$sort: {paper_count: -1}}
    ,{$project:{
            _id:0,
            keywords:'$_id.keywords',
        }
       }
    ,{$limit:30}

);
var top_30 = [];
top_30_keywords.forEach(function (d) {
//     printjson(d);
//     print(d.keywords);
    top_30.push(d.keywords);
//     print(d._id.keywords);
});
print(top_30);
db.getCollection('test').aggregate(
    {'$unwind': '$cleaned_keywords'}
    , 
    {
        $match: {
            cleaned_keywords: {$in:top_30}
        }
    }
    , {
        $group: {
            _id: {'keywords': '$cleaned_keywords','pub_year':'$pub_year'},
            paper_count: {$sum: 1},
        }
    }
    ,{$project:{
        'keywords':'$_id.keywords',
        'paper_count':1,
        'pub_year':'$_id.pub_year',
        '_id':0
     }
 }
    ,{
        $group: {
            _id: {'keywords': '$keywords'},
            year_citations:{$addToSet:'$$ROOT'}
        }
    }
    , {$sort: {paper_count: -1}}
);
