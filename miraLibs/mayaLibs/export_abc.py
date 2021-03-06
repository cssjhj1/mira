# -*- coding: utf-8 -*-
import os
import maya.cmds as mc
import load_plugin


def export_abc(start_frame, end_frame, tar_path, root, uv_write=True, renderable_only=True, attribute=None):
    if isinstance(root, basestring):
        root = [root]
    if isinstance(attribute, basestring):
        attribute = [attribute]
    tar_dir = os.path.dirname(tar_path)
    if not os.path.isdir(tar_dir):
        os.makedirs(tar_dir)
    load_plugin.load_plugin("AbcExport.mll")
    j_base_string = "-frameRange {start_frame} {end_frame} -worldSpace" \
                    " -writeVisibility -file {tar_path}"
    if uv_write:
        j_base_string += " -uvWrite"
    if renderable_only:
        j_base_string += " -renderableOnly"
    if attribute:
        for attr in attribute:
            j_base_string += " -u %s" % attr
    for r in root:
        j_base_string += " -root %s" % r
    j_string = j_base_string.format(start_frame=start_frame, end_frame=end_frame, tar_path=tar_path)
    mc.AbcExport(j=j_string)


if __name__ == "__main__":
    pass
