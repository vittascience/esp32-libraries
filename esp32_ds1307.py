from micropython import const

# I2C-Address - DS1307
RTC_V1_ADDRESS = const(0x68)

# registar overview - crtl & status reg
RTC_CTRL_1 = const(0x00)
RTC_CTRL_2 = const(0x01)

# registar overview - time & data reg
RTC_SECOND_ADDR = const(0x00)
RTC_MINUTE_ADDR = const(0x01)
RTC_HOUR_ADDR   = const(0x02)
RTC_WDAY_ADDR   = const(0x03)
RTC_DAY_ADDR    = const(0x04)
RTC_MONTH_ADDR  = const(0x05)
RTC_YEAR_ADDR	  = const(0x06)

DAY_OF_WEEK = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

class DS1307:
  def __init__(self, i2c, addr=RTC_V1_ADDRESS):
    self._addr = addr
    self._i2c = i2c

  def decToBcd(self, val):
    return (val // 10) << 4 | (val % 10)

  def bcdToDec(self, val):
    return ((val >> 4) * 10) + (val & 0x0F)

  def reset(self):
    self._i2c.writeto_mem(self._addr, RTC_CTRL_1, '\x58')

  def fillByHMS(self, hour, minute, second):
    self._i2c.writeto_mem(self._addr, RTC_SECOND_ADDR, bytearray([self.decToBcd(second)]))
    self._i2c.writeto_mem(self._addr, RTC_MINUTE_ADDR, bytearray([self.decToBcd(minute)]))
    self._i2c.writeto_mem(self._addr, RTC_HOUR_ADDR, bytearray([self.decToBcd(hour)]))

  def fillByYMD(self, year, month, day):
    self._i2c.writeto_mem(self._addr, RTC_DAY_ADDR, bytearray([self.decToBcd(day)]))
    self._i2c.writeto_mem(self._addr, RTC_MONTH_ADDR, bytearray([self.decToBcd(month)]))
    self._i2c.writeto_mem(self._addr, RTC_YEAR_ADDR, bytearray([self.decToBcd(year-2000)]))

  def fillDayOfWeek(self, dayOfWeek):
    self._i2c.writeto_mem(self._addr, RTC_WDAY_ADDR, bytearray([self.decToBcd(DAY_OF_WEEK.index(dayOfWeek))]))

  def startClock(self):
    second = self._i2c.readfrom(self._addr, 1)[0] & 0x7f
    self._i2c.writeto_mem(self._addr, RTC_CTRL_1, bytearray([second]))

  def readTime(self):
    rdata = self._i2c.readfrom_mem(self._addr, RTC_SECOND_ADDR, 7)
    return (
      self.bcdToDec(rdata[6]) + 2000, # year
      self.bcdToDec(rdata[5]), # month
      self.bcdToDec(rdata[4]), # day
      DAY_OF_WEEK[self.bcdToDec(rdata[3])], # weekday
      self.bcdToDec(rdata[2]), # hour
      self.bcdToDec(rdata[1]), # minute
      self.bcdToDec(rdata[0] & 0x7F), # second
  )
