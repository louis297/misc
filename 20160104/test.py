#setting
working_start_hour = 8
working_start_minute = 0
working_end_hour = 17
working_end_minute = 30


class time:
    def __init__(self, dstr, tstr):
        try:
            t = dstr.split('/')
            self.month = int(t[0])
            self.day = int(t[1])
            t = t[2].split(' ')
            self.year = int(t[0])
            t = tstr.split(' ')
            t = t[1].split(':')
            self.hour = int(t[0])
            self.minute = int(t[1])
            self.second = int(t[2])
        except ValueError:
            print '---------------------------'
            print dstr,tstr
            print dstr.split('/')
            #print dstr.split('/')[2].split(' ')
            print '---------------------------'
            exit(-1)
            
    def __gt__(self, other):
        if self.year < other.year:
            return False
        if self.month < other.month:
            return False
        if self.day < other.day:
            return False
        if self.hour < other.hour:
            return False
        if self.minute < other.minute:
            return False
        if self.second < other.second:
            return False
        return True
    def __lt__(self, other):
        if self.year > other.year:
            return False
        if self.month > other.month:
            return False
        if self.day > other.day:
            return False
        if self.hour > other.hour:
            return False
        if self.minute > other.minute:
            return False
        if self.second > other.second:
            return False
        return True

class appointment:
    def __init__(self, single):
        self.facility = single[0]
        self.department = single[1]
        self.provider_id = int(single[2])
        if len(single[3]) > 10 and len(single[4]) > 10:
            self.appointment_date = time(single[3], single[4])
        else:
            self.appointment_date = None
        self.patient_id = single[5]
        self.appointment_type = single[6]
        if len(single[7]) > 10 and len(single[8]) > 10:
            self.booking_date = time(single[7], single[8])
        else:
            self.booking_date = None
        self.show_code = single[9]
        if len(single[10]) > 10 and len(single[11]) > 10:
            self.checkin_date = time(single[10], single[11])
        else:
            self.checkin_date = None

def read_data():
    #set file name and path here
    file_name = 'Untitled6.csv'
    f = open(file_name)
    f_read = f.read().rstrip().split('\n')[2:]
    for single in f_read:
        data_list.append(appointment(single.split(',')))
    f.close()

data_list = []
read_data()
data_length = len(data_list)
after_hour_count = 0
after_hour_effective = 0

#################
#delete illegal data
del_list = []
for i in xrange(data_length):
    if not data_list[i].appointment_date:
        del_list.append(i)
del_list.reverse()
for i in del_list:
    del data_list[i]
data_length = len(data_list)

#sort, according to appointment date
data_list.sort(key = lambda x: x.appointment_date)

for i in xrange(data_length):
    if not data_list[i].appointment_date:
        continue
    if data_list[i].appointment_type == 'Telephone Visit':
        #flag1 means is this call later than working time in the afternoon
        flag1 = data_list[i].appointment_date.hour = working_end_hour and data_list[i].appointment_date.minute >= working_end_minute or data_list[i].appointment_date.hour > working_end_hour + 1
        #flag2 means is this call earlier than working time in the morning
        flag2 = data_list[i].appointment_date.hour = working_start_hour and data_list[i].appointment_date.minute < working_start_minute or data_list[i].appointment_date.hour < working_start_hour
        if flag1 or flag2:
            after_hour_count += 1
            after_hour_effective += 1
            for other in xrange(i+1, data_length):
                #for speed-up, because the data_list is sorted by appointment date
                if data_list[other].appointment_date.day - data_list[i].appointment_date.day > 7:
                    break
                if data_list[other].patient_id == data_list[i].patient_id:
                    after_hour_effective -= 1
                    break


#output
print "Number of patients call in after hour:", after_hour_count
print "Number of patients call in after hour which is effective:", after_hour_effective
print "Effective rate:", float(after_hour_effective) / after_hour_count
            
