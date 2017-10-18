import maya.cmds as mc
import os
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import get_namespace, export_exocortex_abc, get_frame_range
from miraLibs.pipeLibs.pipeMaya.get_assets_under_type_group import get_assets_under_type_group


def export_single_abc(asset):
    context = pipeFile.PathDetails.parse_path()
    mc.parent(asset, world=1)
    namespace = get_namespace.get_namespace(asset)
    abc_name = "%s.abc" % namespace
    abc_path = os.path.join(context.cache_dir, abc_name).replace("\\", "/")
    start, end = get_frame_range.get_frame_range()
    meshes = mc.listRelatives(asset, ad=1, type="mesh")
    geo = [mc.listRelatives(mesh, p=1)[0] for mesh in meshes]
    objects = list(set(geo))
    if os.path.isfile(abc_path):
        export_exocortex_abc.export_exocortex_abc(abc_path, 950, end, objects)
    else:
        cache_dir, base_name = os.path.split(abc_path)
        temp_dir = "%s/tmp" % cache_dir
        if not os.path.isdir(temp_dir):
            os.makedirs(temp_dir)
        temp_path = "%s/%s" % (temp_dir, base_name)
        export_exocortex_abc.export_exocortex_abc(temp_path, start, end, objects)
        os.system('mklink /H "%s" "%s"' % (abc_path, temp_path))


def export_model_abc():
    assets = get_assets_under_type_group("Char")+get_assets_under_type_group("Prop")
    if not assets:
        return
    for asset in assets:
        export_single_abc(asset)


if __name__ == "__main__":
    export_model_abc()
