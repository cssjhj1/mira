# -*- coding: utf-8 -*-
import os
import logging
import maya.cmds as mc
from miraLibs.mayaLibs import new_file, save_as, create_group, quit_maya, Assembly
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import fix_frame_range


def reference_in_env(context):
    set_ad_path = pipeFile.get_task_file(context.project, context.sequence, "c000", "Set", "Set", "maya_shot_definition", "")
    if not os.path.isfile(set_ad_path):
        print "%s is not an exist file" % set_ad_path
        return
    assemb = Assembly.Assembly()
    node_name = "%s_%s_set" % (context.sequence, "c000")
    node = assemb.reference_ad(node_name, set_ad_path)
    create_group.create_group("Env")
    mc.parent(node, "Env")
    return node


def create_references_group():
    create_group.create_group("Char")
    create_group.create_group("Prop")
    create_group.create_group("Temp")


def create_camera(seq, shot):
    create_group.create_group("Camera")
    camera_name = "cam_%s_%s" % (seq, shot)
    cam = mc.camera()
    mc.rename(cam[1], "%sShape" % camera_name)
    camera = mc.rename(cam[0], camera_name)
    mc.parent(camera, "Camera")


def main(file_name, local):
    logger = logging.getLogger("AnimLay start")
    new_file.new_file()
    context = pipeFile.PathDetails.parse_path(file_name)
    seq = context.sequence
    shot = context.shot
    # create camera
    create_camera(seq, shot)
    logger.info("Create camera done.")
    # reference env
    reference_in_env(context)
    logger.info("Reference env done.")
    # create_references_group
    create_references_group()
    logger.info("Create reference group done.")
    # fix frame range
    fix_frame_range.fix_frame_range(context)
    save_as.save_as(file_name)
    logger.info("%s publish successful!" % file_name)
    if not local:
        quit_maya.quit_maya()
