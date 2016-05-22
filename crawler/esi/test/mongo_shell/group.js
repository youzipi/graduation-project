db.getCollection('test').aggregate(
{$unwind:"$authors"}
,
{$group:
    {
        _id:{_id:'$_id','citations':'$citations','wos_no':'$wos_no'},
        author_count:{$sum:1},
//         citations:{$sum:'$citations'}
        }
}
,
{$group:
    {
        _id:'$author_count',
        paper_count:{$sum:1},
        citations_all:{$sum:'$_id.citations'},
        citations_avg:{$avg:'$_id.citations'}
    }
}
,
{$project:
    {
        author_count:"$_id",
        _id:0,
        paper_count:1,
        citations_avg:1

    }
    
}
,
{$sort:{_id:1}}
// {$sort:{paper_count:-1}}

)