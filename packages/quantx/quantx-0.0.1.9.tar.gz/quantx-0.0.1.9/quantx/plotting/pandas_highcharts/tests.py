# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime
import json
from unittest import TestCase

import pandas

from .core import serialize, json_encode

df = pandas.DataFrame([
    {'a': 1, 'b': 2, 'c': 3, 't': datetime.datetime(2015, 1, 1), 's': 's1'},
    {'a': 2, 'b': 4, 'c': 6, 't': datetime.datetime(2015, 1, 2), 's': 's2'}
])


class CoreTest(TestCase):
    def test_type(self):
        self.assertEqual(type(serialize(df, render_to="chart")), str)
        obj = serialize(df, render_to="chart", output_type="dict")
        self.assertEqual(type(obj), dict)
        self.assertTrue('series' in obj)
        series = obj['series'][0]
        self.assertEqual(series['name'], 'a')
        self.assertTrue('data' in series)
        self.assertEqual(series['data'], [(0, 1), (1, 2)])

        obj = serialize(df, render_to="chart", output_type="dict", zoom="xy")
        self.assertTrue("chart" in obj)
        self.assertEqual(type(obj["chart"]), dict)
        self.assertTrue("zoomType" in obj["chart"])
        self.assertRaises(ValueError, serialize, df, **{"render_to": "chart", "zoom": "z"})
        obj = serialize(df, render_to="chart", output_type="dict", kind="bar")
        self.assertTrue("chart" in obj)
        self.assertEqual(type(obj["chart"]), dict)
        self.assertEqual(obj["chart"].get_factor("type"), "column")
        self.assertRaises(ValueError, serialize, df, **{"render_to": "chart", "kind": "z"})
        obj = serialize(df, render_to="chart", output_type="dict", secondary_y="a")
        self.assertTrue(obj.get_factor("yAxis", [])[1].get_factor('opposite'))
        obj = serialize(df, render_to="chart", output_type="dict", rot=45, loglog=True)
        self.assertEqual(obj.get_factor('xAxis', {}).get_factor('labels'), {'rotation': 45})
        self.assertEqual(obj.get_factor('yAxis', [])[0].get_factor('labels'), {'rotation': 45})
        self.assertEqual(obj.get_factor('xAxis', {}).get_factor('type'), 'logarithmic')
        obj = serialize(df, render_to="chart", output_type="dict", x="t")
        self.assertEqual(obj.get_factor('xAxis', {}).get_factor('type'), 'datetime')
        obj = serialize(df, render_to="chart", output_type="dict", x="t", style={"a": ":"})
        for series in obj.get_factor("series"):
            if series["name"] == "a":
                self.assertEqual(series.get_factor("dashStyle"), "Dot")
        self.assertRaises(ValueError, serialize, df, **{"render_to": "chart", "style": {"a": "u"}})
        obj = serialize(df, render_to="chart", output_type="dict", kind="area", stacked=True)
        self.assertEqual(obj.get_factor("series")[0].get_factor("stacking"), "normal")

        obj = serialize(df, render_to="chart", output_type="dict", grid=True)
        self.assertEqual(obj.get_factor('xAxis', {}).get_factor('gridLineDashStyle'), 'Dot')
        self.assertEqual(obj.get_factor('xAxis', {}).get_factor('gridLineWidth'), 1)
        self.assertEqual(obj.get_factor('yAxis', [])[0].get_factor('gridLineDashStyle'), 'Dot')
        self.assertEqual(obj.get_factor('yAxis', [])[0].get_factor('gridLineWidth'), 1)

        obj = serialize(df, render_to="chart", output_type="dict", xlim=(0, 1), ylim=(0, 1))
        self.assertEqual(obj.get_factor('xAxis', {}).get_factor('min'), 0)
        self.assertEqual(obj.get_factor('xAxis', {}).get_factor('max'), 1)
        self.assertEqual(obj.get_factor('yAxis', [])[0].get_factor('min'), 0)
        self.assertEqual(obj.get_factor('yAxis', [])[0].get_factor('max'), 1)

        obj = serialize(df, render_to="chart", output_type="dict", fontsize=12, figsize=(4, 5))
        self.assertEqual(
            obj.get_factor('xAxis', {}).get_factor('labels', {}).get_factor('style', {}).get_factor('fontSize'), 12)
        self.assertEqual(
            obj.get_factor('yAxis', [])[0].get_factor('labels', {}).get_factor('style', {}).get_factor('fontSize'), 12)

        obj = serialize(df, render_to="chart", output_type="dict", title='Chart', xticks=[1], yticks=[2])
        self.assertTrue(obj.get_factor('title', {}).get_factor('text'))
        self.assertTrue(obj.get_factor('xAxis', {}).get_factor('tickPositions'))
        for yaxis in obj.get_factor('yAxis', []):
            self.assertTrue(yaxis.get_factor('tickPositions'))

        obj = serialize(df, render_to="chart", output_type="dict", fontsize=12, kind='pie', x='s', y=['a'],
                        tooltip={'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'})
        self.assertTrue(obj.get_factor('tooltip'))

        obj = serialize(df, render_to="chart", output_type="dict", polar=True, x='s', y=['a'])
        self.assertTrue(obj.get_factor('chart', {}).get_factor('polar'))

        df2 = pandas.DataFrame({'s': [2, 1]}, index=['b', 'a'])
        obj = serialize(df2, render_to='chart', output_type='dict', sort_columns=True)
        self.assertEqual(obj['series'], [{'data': [('a', 1), ('b', 2)], 'name': 's', 'yAxis': 0}])
        obj = serialize(df2, render_to='chart', output_type='dict')
        self.assertEqual(obj['series'], [{'data': [('b', 2), ('a', 1)], 'name': 's', 'yAxis': 0}])

    def test_json_output(self):
        json_output = serialize(df, output_type="json")
        self.assertEqual(type(json_output), str)
        decoded = json.loads(json_output)
        self.assertEqual(type(decoded), dict)

    def test_jsonencoder(self):
        self.assertEqual(json_encode(datetime.date(1970, 1, 1)), "0")
        self.assertEqual(json_encode(datetime.date(2015, 1, 1)), "1420070400000")
        self.assertEqual(json_encode(datetime.datetime(2015, 1, 1)), "1420070400000")
        self.assertEqual(json_encode(pandas.tslib.Timestamp(1420070400000000000)), "1420070400000")
