from ds.vortex import customLogger
import json

logger = customLogger.getCustomLogger()


def loadJson(filePath):
    """
    This procedure loads and returns the data of a json file
    :return type{dict}: the content of the file
    """
    # load our file
    try:
        f = open(filePath)
        data = json.load(f)

    except Exception as er:
        logger.debug("file (%s) not loaded" % filePath)
        raise er
    # return the files data
    return data


def saveJson(data, filepath, **kws):
    """
    This procedure saves given data to a json file
    :param kws: Json Dumps arguments , see standard python docs
    """

    try:
        writeData = json.dumps(data, **kws)
        f = open(filepath, "w")
        f.write(writeData)
        f.close()

    except Exception as er:
        logger.error("Data not saved \n %s >>>" % er)
        return False

    logger.info("------->> file correctly saved to : {0}".format(filepath))

    return True
