import unittest
import json

from lib.Context import Context

class TestContext(unittest.TestCase):

    def test_add_variable(self):
        ctx = Context()
        ctx.addVariable("currentDir", "1")
        res = ctx.getFormated("a/${currentDir}/b")
        self.assertEqual(res, "a/1/b")

    def test_readd_variable(self):
        ctx = Context()
        ctx.addVariable("currentDir", "1")
        ctx.addVariable("currentDir", "2")
        res = ctx.getFormated("${currentDir}")
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

    def test_parent_context(self):
        rootCtx = Context()
        rootCtx.addVariable("a", "1")

        childCtx = Context()
        childCtx.addVariable("b", "2")

        childCtx.setParentContext(rootCtx)
        self.assertEqual(childCtx.getVariable("a"), "1")

    def test_invalid_var_format_0(self):
        ctx = Context()
        ctx.addVariable("a", "1")
        try:
            res = ctx.getFormated("{a}")
        except:
            pass
        else:
            self.fail("Can't fail if invalid format")


    def test_invalid_var_format_1(self):
        ctx = Context()
        ctx.addVariable("a", "1")
        try:
            res = ctx.getFormated("${a")
        except:
            pass
        else:
            self.fail("Can't fail if invalid format")