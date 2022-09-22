
from IOZero32 import IOZero32
import time

def main():
    # Create an instance of the IOZero32 class with an I2C address of 0x20
    iobus1 = IOZero32(0x20)
    iobus2 = IOZero32(0x21)
    # We will write to the pins 9 to 16 so set port 1 to be outputs turn off
    # the pins
    iobus1.set_port_direction(0, 0x00)
    iobus1.set_port_direction(1, 0x00)
    iobus2.set_port_direction(0, 0x00)
    iobus2.set_port_direction(1, 0x00)

    iobus1.write_port(0, 0x00)
    iobus1.write_port(1, 0x00)
    iobus2.write_port(0, 0x00)
    iobus2.write_port(1, 0x00)

if __name__ == "__main__":
    main()
