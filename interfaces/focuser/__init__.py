from astropy.io import fits
import numpy as np
from time import sleep
import serial
import serial.tools.list_ports
import sys

from pywindi.scripts.config import config
from pywindi.windrivers import SBIG_CCD
from pywindi.winclient import Winclient

# --------------------capture function -----------------------#
# after connecting to ccd, this function capretures the 'fits' file and returns the address that the file has been saved

class __Focuser:

    ccd_name = None
    address = None
    image_path = None
    serial = None
    client = None
    focuser_position = None
    state_flag = "disconnected"

    def __init__(self, focuser_id):

        # only for call without argument
        # print (sys.argv[1])
        if str(sys.argv[1]) == 'A':
            print ('Connecting to Module A')
            self.focuser_start('VID:PID=0403:6001SER=A106OMI2')
            self.ccd_name = 'A'
            self.connect(host = '172.18.1.30')
        if sys.argv[1] == 'B':
            print ('Connecting to Module B')
            self.focuser_start('VID:PID=0403:6001SER=AH060RBN')
            self.ccd_name = 'B'
            self.connect(host = '172.18.1.31')
        if sys.argv[1] == 'C':
            print ('Connecting to Module C')
            self.focuser_start('VID:PID=0403:6001SER=AH1MMST5')
            self.ccd_name = 'C'
            self.connect(host = '172.18.1.32')
        #else:
        #    print('There is no ccd with this name!')
        #self.change_focus('RRRRRR')
        if len(sys.argv) == 2:
            self.instruction('begin')
        if len(sys.argv) == 4:
            if int(sys.argv[3]) < 1000:
                self.focuser_position = int(sys.argv[2])
                input_string = self.calculate_string_for_focuser_based_on_position_indexed_from_start(self.focuser_position)
                self.change_focus(input_string)
                self.capture(int(sys.argv[3]))
            else:
                self.binary_search_with_capture(int(self.serial.read(-6)), int(sys.argv[2]), int(sys.argv[3]), self.estimate_exposure_time())


    def __del__(self):
        print('distructed!!!')


    def connect(self, host='localhost', port=7624):  #host = 'localhost'   host='172.18.1.31'
        config('/home/shekarchi/Desktop/images/', '(' + host + ':7624)')
        #config('/home/amirhossein/Desktop/images', '(localhost:7624)')
        file = open('ccd_base_config.txt', 'r')
        self.image_path = file.readline()[:-1]
        addresses = file.readline()[1:-1].replace(' ', '').split(',')
        self.address = addresses[0]
        print(addresses, self.image_path, self.address)
        self.client = Winclient(host, int(port))
        return


    def capture(self, focus_time=5):
        print(self.address)
        print(self.image_path)
        try:
            ccd = self.client.get_device('SBIG CCD')
        except:
            print('Couldn\'t connect to', self.address, 'server.\nI\'m trying again.')
            return None
        if self.address == '172.18.1.30:7624':
            ccdNo = 'CCDA-'
        if self.address == '172.18.1.31:7624':
            ccdNo = 'CCDB-'
        if self.address == '172.18.1.32:7624':
            ccdNo = 'CCDC-'
        ccd.configure(image_directory=(self.image_path + ccdNo))
        return ccd.take_image(focus_time)


    # --------------------focuser_start function -----------------------#
    # this function initiate the focuser #

    def focuser_start(self, focuser_id):
        self.state_flag = "connecting"
        ser = ''
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            ID = p[2].split(' ')
            if len(ID) >= 3:
                ID1 = ID[1] + ID[2]
                print(ID1)
                # if ID1 == 'VID:PID=0403:6001SER=AH060RBM':
                if ID1 == focuser_id:
                    print('Focuser is now detected')
                    print('Connecting to Focuser')
                    ser = serial.Serial(p[0], 115200)
        sleep(7)
        if ser:
            self.serial = ser
        else:
            print('Error in focuser_start function: serial is empty')
        return


    # --------------------change_focus function -----------------------#
    # this function pass a string to the focuser (hardware) and can change the focus #


    def change_focus(self, input_in):
        input_prime = input_in + '\n'
        self.serial.flush()

        sleep(int(len(input_in) / 3) + 1)

        self.serial.write(input_prime.encode())

        # print(self.serial.read(6 * len(input_in)))
        string = str(self.serial.read(6 * len(input_in)))
        print('focuser position: ' + string[-6:-1])
        self.focuser_position = int(string[-6:-1])
        return self.focuser_position



    # --------------------variance_method function -----------------------#
    # this function is the main function for focusing,
    # based on the variance method this function find the best 'focused image' and move the focuser to the best location

    def variance_method(self):
        self.state_flag = "focusing"

        flag = True
        aid = [0, 0]

        focus_time = self.estimate_exposure_time()

        first_image = self.capture(focus_time)
        print(first_image)
        first_image_data = self.read_fits_file(first_image)
        var = np.var(np.asarray(first_image_data))
        print(str(var) + '\n')
        aid[0] = var
        position = self.change_focus('R')
        for i in range(17):
            image = self.capture(focus_time)
            image_data = self.read_fits_file(image)
            var_prime = np.var(np.asarray(image_data))
            print(var_prime)
            if 1.1 * var_prime < var:
                final_position = self.binary_search(var_prime, position, aid[1], position + 200, 'l', focus_time)
                print(final_position)
                print(type(final_position))
                if (int(final_position) % 100 < 5 or int(final_position) % 100 > 95):
                    final_position = self.binary_search_with_capture(final_position, final_position + 20, final_position - 20, focus_time)
                flag = False
                break
            else:
                aid[1] = aid[0]
                aid[0] = var_prime
                var = var_prime
            position = self.change_focus('R')
        if not flag: # if flag == False:
            print("to sorena:   focused bitch :) ")
            self.state_flag = "focused"
            return final_position
        else:
            raise Exception("cannot be focused!")



    # --------------------binary_search function -----------------------#
    # this function finds the exact focus


    def binary_search(self, the_first, position_first, the_second, position_second, direction, focus_time):
        diff = int(abs(position_first - position_second) / 2)
        if diff < 1:
            if the_first > the_second:
                print('focused!!!')
                image = self.capture(focus_time)
                return position_first
            else:
                self.change_focus(direction)
                print('focused!!!')
                image = self.capture(focus_time)
                return position_second

        if direction == 'r':
            direction_prime = 'l'
            B_direction = 'R'
        else:
            direction_prime = 'r'
            B_direction = 'L'
        string_aid = int(diff / 100) * B_direction + direction * int(diff % 100)
        position_prime = self.change_focus(string_aid)

        print("diff = " + str(diff) +  " , dir = " + direction)
        print("var1 = " + str(the_first) + " , position1 = " + str(position_first))
        print("var2 = " + str(the_second) + " , position2 = " + str(position_second))


        image = self.capture(focus_time)
        image_data = self.read_fits_file(image)
        var = np.var(np.asarray(image_data))
        print(str(var) + '\n')
        if the_first > the_second:
            return self.binary_search(var, position_prime, the_first, position_first, direction_prime, focus_time)
        else:
            return self.binary_search(var, position_prime, the_second, position_second, direction, focus_time)



    def binary_search_with_capture(self, the_position, position_first, position_second, focus_time):
        if abs(the_position - position_first) > abs(the_position - position_second):
            direction , op_direction = 'l' , 'r'
            B_direction , B_op_direction = 'L' , 'R'
            diff = abs(the_position - position_first)
        else:
            direction , op_direction = 'r' , 'l'
            B_direction , B_op_direction = 'R' , 'L'
            diff = abs(the_position - position_second)


        string_aid = int(diff / 100) * B_direction + direction * int(diff % 100)
        self.change_focus(string_aid)

        first_image = self.capture(focus_time)
        first_image_data = self.read_fits_file(first_image)
        first_image_var = np.var(np.asarray(first_image_data))
        print('first image variance: ' + str(first_image_var))

        diff = abs(position_first - position_second)
        string_aid = int(diff / 100) * B_op_direction + op_direction * int(diff % 100)
        self.change_focus(string_aid)

        second_image = self.capture(focus_time)
        second_image_data = self.read_fits_file(second_image)
        second_image_var = np.var(np.asarray(second_image_data))
        print('second image variance: ' + str(second_image_var))

        return self.binary_search(second_image_var, position_second, first_image_var, position_first, direction, focus_time)


    # --------------------read_fits_files function -----------------------#
    # this function open the 'fits' file and pass it to the other functions

    def read_fits_file(self, address):
        print(address)
        fits_file = fits.open(address)
        data = fits_file[0].data
        return data

    def estimate_exposure_time(self):
        return 5
        first_image = self.capture()
        focus_image_data = self.read_fits_file(first_image)

        all_data = np.asarray(focus_image_data).ravel()

        upper_bound = 0.95 * 2**16
        lower_bound = 2 * np.median(all_data)

        over_exposed = [i for i in all_data if i > upper_bound]
        under_exposed = [i for i in all_data if i < lower_bound]

        if len(over_exposed) > 0.05 * len(all_data):
            print('estimate time for exposure: 5s')
            return 5
        elif len(under_exposed) > 0.8 * len(all_data):
            print('estimate time for exposure: 13s')
            return 5
        else:
            print('estimate time for exposure: 8s')
            return 5


    def calculate_string_for_focuser_based_on_position_indexed_from_start(self, focuser_position, base=23000):
        MAX = 23000
        MIN = 21000
        if focuser_position > MAX or focuser_position < MIN:
            raise Exception('value must be in range')
        else:
            if base != 23000:
                MAX = base
            if focuser_position - int(focuser_position / 10) * 10 < 5:
                long = int((MAX - focuser_position) / 100)
                short = MAX - long * 100 - focuser_position
                input_string = 'R' * long + 'r' * short
            else:
                long = int((MAX - focuser_position) / 100) + 1
                short = long * 100 - (MAX - focuser_position)
                input_string = 'R' * long + 'l' * short
        return input_string

    ################################################

    ################################################

    def instruction(self, query):
        if query == 'end':
            del self
        elif query == 'begin':
            position = self.variance_method()
            print(position)
        elif query == 'check':
            position = self.binary_search_with_capture(position, position + 25, position - 25, self.estimate_exposure_time())
            print(position)

    def get_focuser_position(self):
        return self.focuser_position


#
# example = Focuser(sys.argv[1])
# print('focuser is ready...')
# #example.instruction('begin')
#
# focuser = __Focuser()

# focusera = Focuser(A, 22006, 21960)
# focuserb = Focuser(B)
# focuserc = Focuser(C,22120, 22054)
