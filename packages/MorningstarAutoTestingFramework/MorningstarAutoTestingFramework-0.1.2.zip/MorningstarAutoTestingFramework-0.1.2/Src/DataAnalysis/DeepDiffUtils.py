# -*- coding: utf-8 -*-
from deepdiff import DeepDiff


tableA = [{"id": 1, "name": "foo"}, {"id": 2, "name": "bar"}]

tableB = [{"id": 1, "name": "bar"}, {"id": 3, "name": "baz"}]

tableA = {item["id"]: item["name"] for item in tableA}
tableB = {item["id"]: item["name"] for item in tableB}

print(DeepDiff(tableA, tableB))
