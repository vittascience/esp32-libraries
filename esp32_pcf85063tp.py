from micropython import const

# I2C-Adresse des PCF80063A
RTC_ADDRESS = const(0x51)

# registar overview - crtl & status reg
RTC_CTRL_1 = const(0x00)
RTC_CTRL_2 = const(0x01)
RTC_OFFSET = const(0x02)
RTC_RAM_by = const(0x03)

# registar overview - time & data reg
RTC_SECOND_ADDR = const(0x04)
RTC_MINUTE_ADDR = const(0x05)
RTC_HOUR_ADDR   = const(0x06)
RTC_DAY_ADDR    = const(0x07)
RTC_WDAY_ADDR   = const(0x08)
RTC_MONTH_ADDR  = const(0x09)
RTC_YEAR_ADDR	  = const(0x0a)

DAY_OF_WEEK = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

class RTC:
  def __init__(self, i2c, addr=RTC_ADDRESS):
    self._addr = addr
    self._i2c = i2c

  def decToBcd(self, val):
    return (val // 10 * 16) + (val % 10)

  def bcdToDec(self, val):
    return (val // 16 * 10) + (val % 16)

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
      self.bcdToDec(rdata[6]) + 2000,
      self.bcdToDec(rdata[5] & 0x1f),
      self.bcdToDec(rdata[3] & 0x3f),
      DAY_OF_WEEK[self.bcdToDec(rdata[4] & 0x07)],
      self.bcdToDec(rdata[2] & 0x3f),
      self.bcdToDec(rdata[1]) & 0x7f,
      self.bcdToDec(rdata[0])
    )
  
