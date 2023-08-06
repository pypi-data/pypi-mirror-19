import datetime
import copy
from GNOMEAcquirerLibs.AttributeData import *

# constants
# The following define error messages definitions, as communicated between the main thread and the acquisition thread
ERROR_SEVERITY_SEVERE  = "Severe"
ERROR_SEVERITY_WARNING = "Warning"

ERROR_IDENTIFIER_SEVERITY = "Severity"
ERROR_IDENTIFIER_MESSAGE  = "Message"


def GetChannelToArrayMapping(channelOpBinary):
    """
    Channel to array mapping is necessary because if a channel is disabled, consequently a column disappears instead
    of making it empty.
    Therefore, it's important to detect what channels are enabled, and then map them in order with the available column.
    ChannelToArray means channel number in the device vs the column number in the array
    :param channelOpBinary: A list with length that is equal to the maximum number of channels (so, 4).
        It contains as boolean flags whether a every channel is enabled
    :return: Returns a dict that has for every enabled channel the corresponding column in the array. If the channel
    doesn't exist, its key doesn't exist in the dict.
    """
    #find channel to array element correspondence. In the acquisition box, if a channel is disabled, it doesn't produce output
    channelToArrayMapping = {}
    chToArrCounter = 0
    #check available channels
    for i in range(len(channelOpBinary)):
        if channelOpBinary[i]:
            channelToArrayMapping[i] = chToArrCounter
            chToArrCounter += 1
    return channelToArrayMapping


def FindDataRange(StrQueue, startStr, endStr):
    startIndex = next((i for i in range(len(StrQueue)) if StrQueue[i].replace(" ","").replace("\t","") == startStr), None)
    if startIndex is not None:
        endIndex = next(
            (i for i in range(startIndex + 1, len(StrQueue)) if StrQueue[i] == endStr), None)
        if endIndex is None:
            raise LookupError("Cannot find " + endStr)
    else:
        raise LookupError("Cannot find " + startStr)
    return startIndex, endIndex+1


# DataBatch is a class whose object contains the data received from the device in a single shot.
# DataBatch consists mainly of a string queue that is received from the device (we call batch here).
# This string queue is analyzed based on a certain order of the information.
class DataBatch:
    SamplingRatePossibilities = [20,50,100,200,500,1000]
    d_dataPrefix       = "@Data"
    d_magneticPrefix   = "@Magnetic"
    d_startString      = "@Header"
    d_endString        = "@End"
    d_timePrefix       = "Time:"
    d_datePrefix       = "Date:"
    d_intTempPrefix    = "Temperature internal [C]:"
    d_extTempPrefix    = "Temperature external [C]:"
    d_latitudePrefix   = "Latitude [deg]:"
    d_longitudePrefix  = "Longitude [deg]:"
    d_altitudePrefix   = "Altitude [m]:"
    d_weekNumberPrefix = "Week number:"
    d_timeNotSetStr = "Time not set!"
    f_dateFormat = "%Y.%m.%d"
    f_timeFormat = "%H.%M.%S"

    def __init__(self, acquisitionConfig, dataQueueOfStrings):
        self.deviceName       = acquisitionConfig.requestedDevice
        self.dataStringQueue  = dataQueueOfStrings
        self.requestedChannelsInDev = acquisitionConfig.requestedChannels
        self.requestedChannelsTypesInDev = acquisitionConfig.requestedChannelsTypes

        self.dataArray        = []
        #Our acquisition system has a built-in (auxiliary) sensor for magnetic fields. These are stored here.
        self.auxMagFieldSensorArray = []
        self.samplingRate     = None
        self.missingPoints    = None
        self.startTime        = None
        self.weekNumber       = None
        self.latitude         = None
        self.longitude        = None
        self.altitude         = None
        self.channelOp        = []
        self.channelOpBinary  = []
        self.receiverMode     = None
        self.intTemperature   = None
        self.extTemperature   = None
        self.magFieldSenorUnit = ""
        self.headerStringList = []
        self.errorFlag = False
        self.errorMsgs = []

        self.parseAllData()


    def containsSevereError(self):
        for err in self.errorMsgs:
            if err[ERROR_IDENTIFIER_SEVERITY] == ERROR_SEVERITY_SEVERE:
                return err
        return None

    def parseAllData(self):
        self.checkParameterInstanceSanity(DataBatch.d_timePrefix)
        self.checkParameterInstanceSanity(DataBatch.d_datePrefix)
        self.checkParameterInstanceSanity(DataBatch.d_intTempPrefix)
        self.checkParameterInstanceSanity(DataBatch.d_extTempPrefix)
        self.checkParameterInstanceSanity(DataBatch.d_latitudePrefix)
        self.checkParameterInstanceSanity(DataBatch.d_longitudePrefix)
        self.checkParameterInstanceSanity(DataBatch.d_altitudePrefix)
        self.checkParameterInstanceSanity(DataBatch.d_weekNumberPrefix)
        if self.errorFlag:
            return self.errorFlag

        if not self.containsSevereError():
            self.parseStartTime()
        if not self.containsSevereError():
            self.parseDataArray()
        if not self.containsSevereError():
            self.parseAuxSensorMagneticFields()
        if not self.containsSevereError():
            self.checkChannelSelectionSanity()
        if not self.containsSevereError():
            self.castDataToCorrectTypes()
        if not self.containsSevereError():
            self.parseCoordinates()
        if not self.containsSevereError():
            self.parseTemperature()
        if not self.containsSevereError():
            self.parseWeekNumber()
        if not self.containsSevereError():
            self.calculateSamplingRate()

        if self.errorFlag:
            return self.errorFlag



    #search string data queue and find a parameter by its prefix.
    #returns a list of lines containing these instances
    def findPrefixInDataQueue(self,prefix):
        return [line for line in self.dataStringQueue if line[:len(prefix)] == prefix]

    #checks whether every parameter exists in every batch only once!
    #a parameter is defined by its prefix in a line
    def checkParameterInstanceSanity(self,prefix):
        dataInstancesCount = sum(line[:len(prefix)] == prefix for line in self.dataStringQueue)
        if dataInstancesCount > 1:
            self.setErrorFlag("Multiple instances of \"" + prefix + "\" string was found in a single data batch. " \
                                                                          "The current model of data " \
                                                                          "includes that only once",ERROR_SEVERITY_SEVERE)
        elif dataInstancesCount == 0:
            self.setErrorFlag("Could not find \"" + prefix + "\" in the current data batch. " \
                                                                   "The current model of the data contains " \
                                                                   "that once per batch.",ERROR_SEVERITY_SEVERE)

    def parseStartTime(self):
        try:
            self.timeStrList = self.findPrefixInDataQueue(self.d_timePrefix)
            self.dateStrList = self.findPrefixInDataQueue(self.d_datePrefix)

            #remove tabs and spaces
            self.timeStr = self.timeStrList[0]
            self.dateStr = self.dateStrList[0]

            # Check if the last part of time equals the timeNotSetStr string, which indicates that GPS is not connected.
            # This part is written after the time string
            if len(self.timeStr) >= len(DataBatch.d_timeNotSetStr):
                if self.timeStr[-len(DataBatch.d_timeNotSetStr):] == DataBatch.d_timeNotSetStr:
                    self.timeStr = self.timeStr[:-len(DataBatch.d_timeNotSetStr)].replace(" ","").replace("\t","")
                    self.setErrorFlag("Time is claimed to be not set. Antenna has to be connected for the data acquired to be meaningful")
                    #return

            self.timeStr = self.timeStr.replace(" ","").replace("\t","")
            self.dateStr = self.dateStr.replace(" ","").replace("\t","")

            #remove strings prefix
            timeStrToParse = self.timeStr.replace(DataBatch.d_timePrefix,"")
            dateStrToParse = self.dateStr.replace(DataBatch.d_datePrefix,"")

            sep = "___"

            try:
                self.startTime = datetime.datetime.strptime(timeStrToParse + sep + dateStrToParse,DataBatch.f_timeFormat + sep + DataBatch.f_dateFormat)
            except Exception as e:
                self.setErrorFlag("Times and Dates are supposed to contain three, two digit numbers separated by a dot, \".\", " \
                                 "This does not seem to be the case! " \
                                 "Check the syntax of the received data from the device. The string seen as time is: " +
                                 "Time: " + str(timeStrToParse) + " | " + "Date: " +str(dateStrToParse) + ". Exception message: " + str(e)
                                  ,ERROR_SEVERITY_SEVERE)
                return

        except Exception as e:
            self.setErrorFlag("An exception was thrown while parsing time. Make sure that the device is sending correct time format." + " Exception message: " + str(e),ERROR_SEVERITY_SEVERE)
            return

    def parseCoordinates(self):
        try:
            longitudeStr = self.findPrefixInDataQueue(self.d_longitudePrefix)[0]
            latitudeStr  = self.findPrefixInDataQueue(self.d_latitudePrefix)[0]
            altitudeStr  = self.findPrefixInDataQueue(self.d_altitudePrefix)[0]

            self.longitude = float(longitudeStr[len(self.d_longitudePrefix):].replace(" ","").replace("\t",""))
            self.latitude  = float(latitudeStr[len(self.d_longitudePrefix):].replace(" ","").replace("\t",""))
            self.altitude  = float(altitudeStr[len(self.d_longitudePrefix):].replace(" ","").replace("\t",""))

        except Exception as e:
            self.setErrorFlag("Could not find/convert coordinates (longitude,latitude,altitude)." + " Exception message: " + str(e),ERROR_SEVERITY_SEVERE)

    def parseTemperature(self):
        try:
            intTempStr = self.findPrefixInDataQueue(self.d_intTempPrefix)[0]
            extTempStr = self.findPrefixInDataQueue(self.d_extTempPrefix)[0]

            self.intTemperature = str(intTempStr[len(self.d_intTempPrefix):].replace(" ","").replace("\t",""))
            self.extTemperature = str(extTempStr[len(self.d_extTempPrefix):].replace(" ","").replace("\t",""))
            try:
                self.intTemperature = float(self.intTemperature)
            except:
                self.intTemperature = "nan"

            try:
                self.extTemperature = float(self.extTemperature)
            except:
                self.extTemperature = "nan"


        except Exception as e:
            self.setErrorFlag("Could not find/convert temperature information." + " Exception message: " + str(e))

    def parseWeekNumber(self):
        try:
            weekNumberStr = self.findPrefixInDataQueue(self.d_weekNumberPrefix)[0]
            self.weekNumber = int(weekNumberStr[len(self.d_weekNumberPrefix):].replace(" ","").replace("\t",""))

        except Exception as e:
            self.setErrorFlag("Could not find/convert week number." + " Exception message: " + str(e), ERROR_SEVERITY_SEVERE)


    def parseDataArray(self):
        try:
            range = FindDataRange(self.dataStringQueue, DataBatch.d_dataPrefix, DataBatch.d_magneticPrefix)
        except Exception as e:
            self.setErrorFlag("Error while searching for auxiliary sensor magnetic field data."
                              + " Exception message: " + str(e))


        self.parseChannelStatusString(self.dataStringQueue[range[0]+1])

        try:
            self.dataArray = list(map(str.split,self.dataStringQueue[range[0]+2:range[1]-1]))
        except Exception as e:
            self.setErrorFlag("Error while pushing acquired data points into an array." + " Exception message: " + str(e),ERROR_SEVERITY_SEVERE)
            return

        # self.getChannelStateBits = False
        # self.startCollecting = False
        # for line in self.dataStringQueue:
        #     if line.replace(" ","").replace("\t","") == DataBatch.d_dataPrefix:
        #         self.getChannelStateBits = True
        #         continue
        #
        #     if self.getChannelStateBits:
        #         self.parseChannelStatusString(line)
        #         self.getChannelStateBits = False
        #         self.startCollecting = True
        #         continue
        #
        #     if self.startCollecting:
        #         if line.replace(" ","").replace("\t","") == DataBatch.d_magneticPrefix:
        #             break
        #         else:
        #             try:
        #                 self.splitLine = line.split()
        #                 self.dataArray.append(self.splitLine)
        #             except Exception as e:
        #                 self.setErrorFlag("Error while pushing acquired data points into an array." + " Exception message: " + str(e),ERROR_SEVERITY_SEVERE)
        #                 return

    def parseAuxSensorMagneticFields(self):

        try:
            range = FindDataRange(self.dataStringQueue, DataBatch.d_magneticPrefix, DataBatch.d_endString)
        except Exception as e:
            self.setErrorFlag("Error while searching for auxiliary sensor magnetic field data."
                              + " Exception message: " + str(e))

        try:
            self.parseAuxMagneticFieldsStatus(self.dataStringQueue[range[0]+1])
            self.auxMagFieldSensorArray = list(map(lambda p: np.array(list(map(np.float32,p.split()))),self.dataStringQueue[range[0]+2:range[1]-1]))

        except Exception as e:
            self.setErrorFlag("Error while pushing auxiliary sensor magnetic field data points into an array."
                              " It is possible that the sensor is not properly connected." + " Exception message: " + str(e))
            return

        # self.getMagStateBits = False
        # self.startCollecting = False
        # for line in self.dataStringQueue:
        #     if line.replace(" ","").replace("\t","") == DataBatch.d_magneticPrefix:
        #         self.getMagStateBits = True
        #         continue
        #
        #     if self.getMagStateBits:
        #         self.parseAuxMagneticFieldsStatus(line)
        #         self.getMagStateBits = False
        #         self.startCollecting = True
        #         continue
        #
        #     if self.startCollecting:
        #         if line.replace(" ","").replace("\t","") == DataBatch.d_endString:
        #             break
        #         else:
        #             try:
        #                 self.splitLine = list(map(np.float32,line.split()))
        #                 self.auxMagFieldSensorArray.append(np.array(self.splitLine))
        #             except Exception as e:
        #                 self.setErrorFlag("Error while pushing auxiliary sensor magnetic field data points into an array."
        #                                   " It is possible that the sensor is not properly connected." + " Exception message: " + str(e))
        #                 return

    def castDataToCorrectTypes(self):
        self.dataArrayTranspose = list(map(list, list(zip(*self.dataArray))))

        self.channelToArrayMapping = GetChannelToArrayMapping(self.channelOpBinary)

        self.dataToSave = {}
        self.channelRangesPerName = {}
        for dataset in self.requestedChannelsInDev:
            try:
                dataArrayIndex = self.channelToArrayMapping[self.requestedChannelsInDev[dataset]-1]
                self.dataToSave[dataset] = self.dataArrayTranspose[dataArrayIndex]

                #save channel ranges from channel name (instead of number)
                self.channelRangesPerName[dataset] = self.channelRanges[self.requestedChannelsInDev[dataset]-1]
            except Exception as e:
                print("Error: Exception with: " + dataset + ": ",e)
                self.setErrorFlag("Error while resorting data from recorded arrays. Make sure you enabled the channels "
                                  "you requested from the acquisition box. Check the data log to find the problem in the data." + " Exception message: " + str(e),ERROR_SEVERITY_SEVERE)
                return
            try:
                if self.requestedChannelsTypesInDev[dataset] == GetTypeNameString(AttributeType.Double):
                    typeToCast = np.float64
                elif self.requestedChannelsTypesInDev[dataset] == GetTypeNameString(AttributeType.Float):
                    typeToCast = np.float32
                elif self.requestedChannelsTypesInDev[dataset] == GetTypeNameString(AttributeType.Integer32):
                    typeToCast = np.int32
                elif self.requestedChannelsTypesInDev[dataset] == GetTypeNameString(AttributeType.Integer64):
                    typeToCast = np.int64
                elif self.requestedChannelsTypesInDev[dataset] == GetTypeNameString(AttributeType.String):
                    typeToCast = np.str
                else:
                    print("Dataset received: " + str(self.dataToSave[dataset]))
                    dataSampleForException = self.dataToSave[dataset][0:4] if len(self.dataToSave[dataset]) > 4 else self.dataToSave[dataset]
                    self.setErrorFlag("No supported data type was found to cast dataset " + dataset + " to " + self.requestedChannelsTypesInDev[dataset] + ". Check the terminal log of the program to see what the full data array looks like. Part of the data is " + str(dataSampleForException) + ". Exception message: " + str(e),ERROR_SEVERITY_SEVERE)
                    print(self.dataToSave)

                # self.dataToSave[dataset] = (np.asarray(self.dataToSave[dataset],dtype=typeToCast) + typeToCast(self.chOffsets[dataset]))*typeToCast(self.conversionFactors[dataset])
                self.dataToSave[dataset] = (np.asarray(self.dataToSave[dataset],dtype=typeToCast))

            except Exception as e:
                print(self.requestedChannelsInDev)
                print(self.dataToSave)
                print("Dataset received: " + str(self.dataToSave[dataset]))
                print("Exception message: ",e)
                dataSampleForException = self.dataToSave[dataset][0:4] if len(self.dataToSave[dataset]) > 4 else self.dataToSave[dataset]
                self.setErrorFlag("Error while trying to cast data of dataset " + dataset + " to " + self.requestedChannelsTypesInDev[dataset] + ". Check the terminal log of the program to see what the full data array looks like. Part of the data is " + str(dataSampleForException) + ". Exception message: " + str(e),ERROR_SEVERITY_SEVERE)


    def parseChannelStatusString(self,chString):
        self.splitChannelStatus = chString.split(",")
        if not len(self.splitChannelStatus) == 4:
            self.setErrorFlag("The line coming directly after " + DataBatch.d_dataPrefix + " is expected"
                              " to contain 4 strings separated by commas. This was not found. Unknown error!",ERROR_SEVERITY_SEVERE)
            return

        else:
            for ch in self.splitChannelStatus:
                chStripped = ch.replace(" ","").replace("\t","")
                #the following removes the prefix strings of channels status, i.e., Ch1, for example.
                self.channelOp.append(chStripped[3:])
        #convert channel findings to binary values
        self.channelOpToBin()
        self.channelOpToRanges()
        # print(self.channelOpBinary)

    def parseAuxMagneticFieldsStatus(self,magString):
        self.magFieldSenorStatus = magString.split()
        if len(self.magFieldSenorStatus) < 4:
            self.setErrorFlag("The header of sensor magnetic fields that comes after " + DataBatch.d_magneticPrefix + " is expected"
                              " to contain 4 or more strings separated by a space. This was not found. "
                              "The string seen is: \"" + magString + "\".", ERROR_SEVERITY_SEVERE)
            return

        else:
            #the range comes 4th
            self.magFieldSenorRange = self.magFieldSenorStatus[3]
            if len(self.magFieldSenorStatus) > 4:
                self.magFieldSenorUnit  = self.magFieldSenorStatus[4].replace("[","").replace("]","")
        # print(self.channelOpBinary)


    #write channel states as booleans
    def channelOpToBin(self):
        #self.channelOp contains whether channels are on or off as strings, it's either "off" or a range
        self.channelOpBinary = list(map(lambda channelStrStatus: True if not channelStrStatus == "off" else False, self.channelOp))

    def channelOpToRanges(self):
                #initialize an array with garbage (meaningless) values. This is because python doesn't have a resize function
        #in its default array
        self.channelRanges = self.channelOp

    def checkChannelSelectionSanity(self):
        self.channelToArrayMapping = GetChannelToArrayMapping(self.channelOpBinary)
        channelCount = 0
        for dataset in self.requestedChannelsInDev:
            binVal = self.channelOpBinary[channelCount]
            if binVal:
                if not (self.requestedChannelsInDev[dataset]-1 in self.channelToArrayMapping):
                    self.setErrorFlag("Error in channel presence. Channel " + str(self.requestedChannelsInDev[dataset]) + " in device " + str(self.deviceName) + " is not enabled and/or does not exist in the acquired data.",ERROR_SEVERITY_SEVERE)
                    print("Error in channel selection. Channel " + str(self.requestedChannelsInDev[dataset]) + " in device " + str(self.deviceName) + " is not enabled and/or does not exist in the acquired data.")

            channelCount += 1

    def calculateSamplingRate(self):
        if len(self.dataArray) < 15:
            self.setErrorFlag("The sampling rate of the data cannot be calculated before parsing the data points. "
                              "Or: You cannot choose a sampling rate that is less than 20 Hz. This is due to the algorithm "
                              "used to calculate the sampling rate and determine whether there are missing points in the data.",ERROR_SEVERITY_SEVERE)
        else:
            try:
                #the following is an algorithm that detects the existence of missing points by comparing with the possible
                #values of the sampling rate
                self.dataLength = len(self.dataArray)
                self.ident = list(map(lambda x: abs(x - self.dataLength), DataBatch.SamplingRatePossibilities))
                self.missingPoints = min(self.ident)
                self.samplingRate = DataBatch.SamplingRatePossibilities[self.ident.index(self.missingPoints)]
                if self.missingPoints != 0:
                    self.setErrorFlag("WARNING: There are missing data points in one of the data batches. Number of missing points is: " + str(self.missingPoints),severity=ERROR_SEVERITY_SEVERE)
            except Exception as e:
                self.setErrorFlag("An exception was thrown while trying to calculate the sampling rate. Exception message: " + str(e),ERROR_SEVERITY_SEVERE)
                print("An exception was thrown while trying to calculate the sampling rate. Exception message: " + str(e))

    def setErrorFlag(self,message,severity=ERROR_SEVERITY_WARNING):
        self.errorFlag = True
        self.errorMsgs.append({ERROR_IDENTIFIER_MESSAGE:message, ERROR_IDENTIFIER_SEVERITY:severity})
