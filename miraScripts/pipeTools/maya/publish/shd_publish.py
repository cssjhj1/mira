# -*- coding: utf-8 -*-
import optparse
import logging
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file, quit_maya, export_selected, \
    import_load_remove_unload_ref, delete_history, delete_unused_nodes, delete_layer
from miraLibs.pipeLibs.pipeMaya import rename_pipeline_shape


def main():
    logger = logging.getLogger("shd publish")
    file_path = options.file
    open_file.open_file(file_path)
    # get paths
    obj = pipeFile.PathDetails.parse_path(file_path)
    project = obj.project
    publish_path = obj.publish_path
    # import all reference
    import_load_remove_unload_ref.import_load_remove_unload_ref()
    logger.info("Import all reference.")
    # delete history and delete unused nodes
    delete_history.delete_history()
    delete_unused_nodes.delete_unused_nodes()
    # rename shape
    if not rename_pipeline_shape.rename_pipeline_shape():
        raise RuntimeError("Rename shape error.")
    # export _MODEL to publish path
    delete_layer.delete_layer()
    export_selected.export_selected(publish_path)
    logger.info("Save to %s" % publish_path)
    quit_maya.quit_maya()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="maya file ma or mb.", metavar="string")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    options, args = parser.parse_args()
    if len([i for i in ["file_name"] if i in dir()]) == 1:
        options.file = file_name
        main()