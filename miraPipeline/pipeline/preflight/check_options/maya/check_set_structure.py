# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.pipeLibs import pipeFile


class Check(BaseCheck):
    def __init__(self):
        super(Check, self).__init__()
        context = pipeFile.PathDetails.parse_path()
        self.model_name = "%s_env" % context.sequence

    def run(self):
        if not mc.objExists(self.model_name):
            self.fail_check(u"大组%s不存在" % self.model_name)
            return
        self.error_list = self.get_error_list()
        if self.error_list:
            self.fail_check(u"这些物体在大组之外，必须删除。")
        else:
            self.pass_check(u"大纲层级结构正确。")

    def get_error_list(self):
        extra = ['persp', 'top', 'front', 'side', self.model_name]
        error_list = list()
        outliner = mc.ls(assemblies=1)
        for i in outliner:
            if i not in extra:
                error_list.append(i)
        return error_list

    def auto_solve(self):
        error_list = self.get_error_list()
        self.error_list = list()
        for i in error_list:
            try:
                mc.delete(i)
            except:
                self.error_list.append(i)
        if self.error_list:
            self.fail_check(u"这些东西不能删除。")
        else:
            self.pass_check(u"多余物体已被删除。")
