db.test.aggregate([
    {
        $unwind: "$research_areas"
    },
    {
        $lookup: {
            from: "test",
            localField: "_id",
            foreignField: "_id",
            as: "items"
        }
    },
    {
        $unwind: "$items"
    },
    {
        $unwind: "$items.research_areas"
    },
    {
        $redact: {
            $cond: {
                if: {
                    $cmp: ["$research_areas", "$items.research_areas"]
                },
                then: "$$DESCEND",
                else: "$$PRUNE"
            }
        }
    },
    {
        $group: {
            _id: {
                k1: "$research_areas",
                k2: "$items.research_areas",
            },
            items: {
                $sum: 0.5
            }
        }
    },
    {
        $sort: {
            "_id": 1
        }
    },
    {
        $project: {
            _id: 1,
            items: 1,
            a: {
                $cond: {
                    if: {
                        $eq: [{
                            $cmp: ["$_id.k1", "$_id.k2"]
                        }, 1]
                    },
                    then: "$_id.k2",
                    else: "$_id.k1"
                }
            },
            b: {
                $cond: {
                    if: {
                        $eq: [{
                            $cmp: ["$_id.k1", "$_id.k2"]
                        }, -1]
                    },
                    then: "$_id.k2",
                    else: "$_id.k1"
                }
            },

        }
    },
    {
        $group: {
            _id: {
                k1: "$a",
                k2: "$b",
            },
            items: {
                $sum: "$items"
            }
        }
    },
    {
        $project: {
            _id: 0,
            source: "$_id.k1",
            target: "$_id.k2",
            count: "$items"
        }
    },
    {
        $sort: {
            count: -1,
        }
    },
    {
        $out: 'area_relation',
    }
])


a =
{ '论文题目':'计算机类ESI数据采集系统设计',
  '作者':{
    '学号':20121344018,
    '姓名':'吴乾泰',
    '专业':'软件工程'
  },
  '指导老师':'闫雷鸣'
};

