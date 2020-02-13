import unittest
import json

from lib.Context import Context

class TestContext(unittest.TestCase):

    def test_add_variable(self):
        ctx = Context()
        ctx.addVariable("currentFile", "1")
        res = ctx.getFormated("a/${currentFile}/b")
        self.assertEqual(res, "a/1/b")

    def test_readd_variable(self):
        ctx = Context()
        ctx.addVariable("currentFile", "1")
        ctx.addVariable("currentFile", "2")
        res = ctx.getFormated("${currentFile}")
        self.assertEqual(res, "2")

    def test_add_two_variable(self):
        ctx = Context()
        ctx.addVariable("a", "linux")
        ctx.addVariable("b", "release")
        res = ctx.getFormated("${a}/${b}")
        self.assertEqual(res, "linux/release")

    def test_add_varible_format(self):
        ctx = Context()
        ctx.addVariable("a", "a")
        ctx.addVariable("b", "${a}/b")
        res = ctx.getFormated("${b}/c")
        self.assertEqual(res, "a/b/c")

    def test_update_dict_for_step(self):
        ctx = Context()
        ctx.addVariable("a", "a")
        data = {"a":"${a}"}
        res = ctx.createStepNode(data)
        self.assertEqual(res["a"], "a")

    def test_update_list_for_step(self):
        ctx = Context()
        ctx.addVariable("a", "a")
        data = {"a":["${a}"]}
        res = ctx.createStepNode(data)
        self.assertEqual(res["a"][0], "a")
