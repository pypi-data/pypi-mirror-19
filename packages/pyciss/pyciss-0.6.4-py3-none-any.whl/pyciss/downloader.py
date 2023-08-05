from . import opusapi


def get_file_id(file_id):
    opus = opusapi.OPUS()
    opus.query_image_id(file_id)
    basepath = opus.download_results()
    print("Downloaded images into {}".format(basepath))
