import os
import glob
import time
import subprocess
import socket
import struct
import binascii

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# ===updated by rocky at 2016-07-08 start===
# ===============TCP Socket Helper start=============== #

DEBUG = True

DST_SERVER_IP = 'localhost'
DST_SERVER_PORT = 55056

backlog = 5
data_payload=2048
temperature = '25.68'

#packer = struct.Struct('!H H f')


def get_tcp_socket():
    server_address = (DST_SERVER_IP, DST_SERVER_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (DST_SERVER_IP, DST_SERVER_PORT)
    #sock.connect(server_address)
    sock.bind(server_address)
    sock.listen(backlog)
    return sock


#def send_data2server(data):
#    sock = None
#    try:
#        sock = get_tcp_socket()
#        packed_data = packer.pack(*data)
#        sock.sendall(packed_data)
#        if DEBUG:
#            print('Succeed in sending "{} {}" to {}'.
#                  format(binascii.hexlify(packed_data), data, sock.getpeername()))
#    except Exception as e:
#        print('Error:', e)
#    finally:
#        if sock:
#            sock.close()


# ===============TCP Socket Helper end=============== #
# check and send data interval(in seconds)
#CHECK_INTERVAL = 1
# mark the device with unique id(This id should be registered on http://115.28.150.131:20180/)
#DEVICE_ID = 1
# mark the sensor with unique id(This id should be registered on http://115.28.150.131:20180/)
#SENSOR_ID = 1
# ===added by rocky at 2016-07-06 end===


def read_temp_raw():
        catdata = subprocess.Popen(['cat',device_file],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err = catdata.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines

def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] !='YES':
                time.sleep(0.2)
                lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos !=-1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c *9.0 / 5.0 +32.0
                #return temp_c , temp_f
                return temp_c

#sum=0
#i=0
while True:
    sock = None
    try:
        sock = get_tcp_socket()
        print 'Waiting to receiving message from client'
        client, address = sock.accept()
        data_from_hass = client.recv(data_payload)
        if data_from_hass:
            print 'Receive Data: %s ' % data_from_hass
            # there is big difference comapare to sock.sendall(msg) in the client
            #packed_data = packer.pack(*data)
            #sock.sendall(packed_data)
            temperature=read_temp()
            client.send(temperature)
            print 'Sent: %s back to %s' % (temperature, address)
    except Exception as e:
	print('Error:', e)
    finally:
        #if sock:
        #    sock.close()
        client.close()


            #a=read_temp()
            #sum=sum+a
            #i+=1
            ##time.sleep(5)
            ##print('the sum is %d' %sum)
            ##print('the read_temp() is %f' % read_temp())
            ##print('the times is %d' %i)
            ##print('')
            #if i > 5:
            #            average=sum/i
            #            sum=0
            #            i=0
            #            print('the average is %f' %average)
            #            data = (DEVICE_ID, SENSOR_ID,average)
            #            send_data2server(data)

            #time.sleep(5)
