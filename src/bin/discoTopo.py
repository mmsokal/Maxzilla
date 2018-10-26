#!/usb/bin/python
import xml.etree.ElementTree as Xet
import argparse as ap
import sys


myVersion = '1.0-1'


class WMTopologyDiscovery:
    def __init__(self, nbi_locationpath):
        self.EMSInfo = {}
        self.NODEInfo = []

        self.__TopologyFile = nbi_locationpath.rstrip('/') + '/periodic/Topology/Topology.xml'
        self.__NodeInfoHeaders = ['NodeId', 'NodeName', 'NodeParent', 'NodeType', 'Status', 'DbVersion',
                                  'CheckedOutRelease', 'SwRelease', 'ActiveRelease', 'Address', 'MacAddress',
                                  'apVlanId', 'CarrierId', 'SectorId', 'TargetNodeId', 'TargetNodeName',
                                  'NeighborNodeId', 'NeighborNodeName', 'ClaProtocolVer', 'ExpiryDate', 'FileName',
                                  'Region', 'wmanCapcFruSlot', 'wmanCapcIfTableIndex', 'wmanCapcLogicalId',
                                  'wmanIfBsPagingGroupId']

        self.__EMSInfoHeaders = ['exportTimestamp', 'exportVersion', 'emsIPAddress', 'emsName', 'emsSoftwareVersion']

        try:
            self.__fopen()
        except FileNotFoundError:
            pass
        else:
            self.__ParseEMSInfo()
            self.__getNodeInfo()
    ###################################################################################################################

    def __convertTimestamp(self, wmTimestamp: str):
        """
        This function converts the timestamps to candle timestamp format
        Note: it will completely ignore TZ informed in the string timestamp

        :param wmTimestamp: Timestamp in the format found in the XMLs '2018-09-18T01:30:03.328'
        :return: Timestamp converted to candle timestamp format '1180918013003328'
        """
        if len(wmTimestamp) >= 23:
            timestamp = '1' + \
                        wmTimestamp[2:4] + \
                        wmTimestamp[5:7] + \
                        wmTimestamp[8:10] + \
                        wmTimestamp[11:13] + \
                        wmTimestamp[14:16] + \
                        wmTimestamp[17:19] + \
                        wmTimestamp[20:23]
        else:
            timestamp = wmTimestamp
        return timestamp
    ###################################################################################################################

    def __fopen(self):
        self.__froot = Xet.parse(self.__TopologyFile).getroot()
    ###################################################################################################################

    def __ParseEMSInfo(self):

        self.EMSInfo = {}
        for child in self.__froot.iter('NETWORK'):
            record = {}
            for key in self.__EMSInfoHeaders:
                if key == 'exportTimestamp':
                    record[key] = self.__convertTimestamp('' if child.attrib.get(key) is None else child.attrib.get(key))
                else:
                    record[key] = '' if child.attrib.get(key) is None else str(child.attrib.get(key))
            self.EMSInfo = record
    ###################################################################################################################

    def __getNodeInfo(self):
        self.NODEInfo = []

        for child in self.__froot.iter('NodeInfo'):
            record = {}
            for key in self.__NodeInfoHeaders:
                if key == 'ActiveRelease' or key == 'ExpiryDate':
                    record[key] = self.__convertTimestamp('' if child.attrib.get(key) is None
                                                          else child.attrib.get(key))
                else:
                    record[key] = '' if child.attrib.get(key) is None else str(child.attrib.get(key))

            self.NODEInfo.append(record)
    ###################################################################################################################

    def ShowEMSInfo(self):
        """
        This function will print to stdout the information collected regarding the EMS from the XML file. It
        corresponds to "NETWORK" Tag found in the file.

        :return: none
        """
        header = ""
        for key in self.__EMSInfoHeaders:
            header += key + ';'
        print(header.rstrip(';'))

        for EMSInfoDic in [self.EMSInfo]:
            record = ""
            for key in self.__EMSInfoHeaders:
                record += EMSInfoDic[key] + ';'
            print(record.rstrip(';'))
        return None
    ###################################################################################################################

    def ShowNodeInfo(self):
        """
        This function will print to stdout the information collected regarding the nodes from the XML file. Those
        correspond to all "NodeInfo" Tags found in the file.

        :return: none
        """
        header = ""
        for key in self.__NodeInfoHeaders:
            header += key + ';'
        print(header.rstrip(';'))

        for NodeInfoDic in self.NODEInfo:
            record = ""
            for key in self.__NodeInfoHeaders:
                record += NodeInfoDic[key] + ';'
            print(header.rstrip(';'))
            print(record.rstrip(';'))
        return None


parser = ap.ArgumentParser(description="This is part of the monitoring of WiMax. It was developed to work as a " +
                                       "replacement for Maxzilla. \nThis processes the 'Tolopogy.xml'.")
parser.add_argument('-v', '--version', action='version', version='%s v%s' % (sys.argv[0], myVersion),
                    help="Display the version of this program")
parser.add_argument('nbiPath', metavar='PATH_TO_NBI', type=str,
                    help="Path to the NBI. The 'periodic/Topoloy/Topology.xml' must exist within.")
#
# Define a exclusive group, the user must select '-e' or '-n'. If none or both are selected it will return an error.
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-n', '--node-info', action='store_true', dest='nodeInfo',
                   help="Collect and display information related to the CAPC, AP, PL, SECTORS, etc...")
group.add_argument('-e', '--ems-info', action='store_true', dest='emsInfo',
                   help="Collect and display information related to the EMS.")
args = parser.parse_args()
#
# Instanciate the class passing the PATH TO NBI as parameter
wm = WMTopologyDiscovery(args.nbiPath)
#
# Call methods depending on which option was specified in the command line
wm.ShowEMSInfo() if args.emsInfo else wm.ShowNodeInfo()
