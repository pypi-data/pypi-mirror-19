#RTK.GPIO implementation of SMBUS
import rtkserial
from pprint import pprint
from time import sleep
serial = rtkserial.s
print("imported rtkbus")
i = 0.0017
class SMBus:

    def __init__(self,bus):
        self.bus = bus
    def _write(self,str):
        #print((str))
        serial.write(str)
    def _read(self, maxsize=1, minsize=None, termset=None, timeout=None):
        if minsize == None:
          minsize = maxsize

        remaining = maxsize
        if termset != None:
          readsz = 1
        else:
          readsz = remaining

        buf = b''

        while len(buf) < minsize:
          data = serial.read(readsz)
          if (len(data) == 0):
              time.sleep(0.1) # prevent CPU hogging
          else:
              #print("just read:" + data)
              buf = buf + data
              remaining -= len(data)
              if termset != None:
                  if data[0] in termset:
                      break # terminator seen

        return buf

    def write_i2c_block_data(self,i2caddress,command,data):
        #Get the address and convert it to 8 bit for mbed and then convert to the char to send over.
        i2caddrchar = chr(int(hex(i2caddress<<1),0))
        #and now convert that to a letter
        self._write("IW") #I2C write
        self._write(i2caddrchar) # Write the 8 Bit I2C address
        self._write(chr(int(len(data))))
        self._write(chr(int(hex(command),0))) # Write the command char
        for idx, dataVal in enumerate(data): #Write each item of data
            self._write(chr(int(hex(dataVal),0))) #Data
            sleep(i)
    def write_byte_data(self,i2caddress,command,data):
        #Get the address and convert it to 8 bit for mbed and then convert to the char to send over.
        i2caddrchar = chr(int(hex(i2caddress<<1),0))
        #and now convert that to a letter
        self._write("IW") #I2C write
        self._write(i2caddrchar) # Write the 8 Bit I2C address
        self._write(chr(int(1)))
        self._write(chr(int(hex(command),0))) # Write the command char
        self._write(chr(int(hex(data),0))) #Data
        sleep(i)

    def write_word_data(self,i2caddress,command,data):
        #Get the address and convert it to 8 bit for mbed and then convert to the char to send over.
        i2caddrchar = chr(int(hex(i2caddress<<1),0))
        #and now convert that to a letter
        self._write("IW") #I2C write
        self._write(i2caddrchar) # Write the 8 Bit I2C address
        self._write(chr(int(1)))
        self._write(chr(int(hex(command),0))) # Write the command char
        self._write(chr(int(hex(data),0))) #Data
        sleep(i)

    def write_byte(self,i2caddress,command):
        #Get the address and convert it to 8 bit for mbed and then convert to the char to send over.
        i2caddrchar = chr(int(hex(i2caddress<<1),0))
        #and now convert that to a letter
        self._write("IW") #I2C write
        self._write(i2caddrchar) # Write the 8 Bit I2C address
        self._write(chr(int(0)))
        self._write(chr(int(hex(command),0))) # Write the command char
        #self._write(chr(int(hex(data),0))) #Datas
        sleep(i)

    def read_word_data(self,i2caddress,command) :
        #Get the address and convert it to 8 bit for mbed and then convert to the char to send over.
        i2caddrchar = chr(int(hex(i2caddress<<1),0))
        self._write("IR") #I2C Read
        self._write(i2caddrchar)
        self._write(chr(int(hex(command),0)))
        wordDat1 =int(serial.read().encode("hex"))
        wordDat2 = int(serial.read().encode("hex"))
        #return(wordDat2)
        wordDat = int(hex((wordDat2<<8)+wordDat1),0)
        sleep(i)

        return(wordDat)
    def read_byte(self,i2caddress):
        pass

    def read_block_data(self,i2caddress,command):
        pass
    def read_byte_data(self,i2caddress,command):
        pass
