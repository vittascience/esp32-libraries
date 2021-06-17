import utime

HM330_I2C_ADDR = 0x40
HM330_INIT = 0x80
HM330_MEM_ADDR = 0x88

class HM330X:

  def __init__(self, i2c, addr=HM330_I2C_ADDR):
    self._i2c = i2c
    self._addr = addr
    self._write([HM330_INIT])

  def read_data(self):
    return self._i2c.readfrom_mem(self._addr, HM330_MEM_ADDR, 29)

  def _write(self, buffer):
    self._i2c.writeto(self._addr, bytearray(buffer))

  def check_crc(self, data):
    sum=0
    for i in range(29-1):
      sum+=data[i]
    sum=sum&0xff
    return (sum==data[28])

  def parse_data(self, data):
    std_PM1=data[4]<<8|data[5]
    std_PM2_5=data[6]<<8|data[7]
    std_PM10=data[8]<<8|data[9]
    atm_PM1=data[10]<<8|data[11]          
    atm_PM2_5=data[12]<<8|data[13]
    atm_PM10=data[14]<<8|data[15]
    return [std_PM1,std_PM2_5,std_PM10,atm_PM1,atm_PM2_5,atm_PM10]

  def getData(self, select):
    datas=self.read_data()
    utime.sleep_ms(5)
    if(self.check_crc(datas)==True):
      data_parsed=self.parse_data(datas)
      return data_parsed[select]
