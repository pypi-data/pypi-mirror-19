from core import getNagiosObject
from core import get_hoststatus_list
from core import get_servicestatus_list
from core import checkFile

class Presentation():
    def __init__(self, PATH):
        checkFile(PATH)
        self.title_head = ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("Component",
                                                                                 "HOST",
                                                                                 "Service",
                                                                                 "STATE",
                                                                                 "OUPUT",
                                                                                 "NOTIFICATION_STATUS",
                                                                                 "COMMENT_ENTRY_TIME",
                                                                                 "COMMENT_AUTHOR",
                                                                                 "COMMENT_DATA",
                                                                                 "DOWNTIME_START",
                                                                                 "DOWNTIME_END",
                                                                                 "DOWNTIME_DURATION",
                                                                                 "IS_DOWNTIME",
                                                                                 "IS_ACKNOWLEDGED",
                                                                                 "DOWNTIME_AUTHOR",
                                                                                 "DOWNTIME_COMMENT"))


        self.nagcfg = getNagiosObject(PATH)
        self.host_status_list = get_hoststatus_list(self.nagcfg)
        self.service_status_list = get_servicestatus_list(self.nagcfg)

    def printAll(self):
        print self.title_head
        for host_status in self.host_status_list:
            print host_status
        for service_status in self.service_status_list:
            print service_status

    def writeToFile(self, output_file):
        try:
            fo = open(output_file, "w")
            fo.write(self.title_head)
            fo.write("\n")
            for host_status in self.host_status_list:
                fo.write(host_status)
                fo.write("\n")
            for service_status in self.service_status_list:
                fo.write(service_status)
                fo.write("\n")
            fo.close()
            return True
        except:
            return False

    def printPrettyTable(self):
        pass
