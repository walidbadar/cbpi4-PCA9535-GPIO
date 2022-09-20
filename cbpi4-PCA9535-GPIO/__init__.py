# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
# import PCA9535_io
from IOZero32 import IOZero32
from cbpi.api import *
from cbpi.api.config import ConfigType
from cbpi.api.dataclasses import Props
from cbpi.api.base import CBPiBase

logger = logging.getLogger(__name__)


# creates the PCF_IO object only during startup. All sensors are using the same object
def PCFActor_1(address):
    global p1

    logger.info("***************** Start PCF Actor on I2C address {} ************************".format(hex(address)))
    try:
        # create to object with the defined address
        # p1 = PCA9535_io.PCF(address)
        p1 = IOZero32(address)  # use address 0x20
        # All pins are set to input at start -> set them to output and low
        p1.set_port_direction(0, 0x00)
        p1.set_port_direction(1, 0x00)
        p1.write_port(0, 0x00)
        p1.write_port(1, 0x00)
        pass
    except:
        p1 = None
        logging.info("Error. Could not activate PCA9535_1 on I2C address {}".format(address))
        pass


def PCFActor_2(address):
    global p2

    logger.info("***************** Start PCF Actor on I2C address {} ************************".format(hex(address)))
    try:
        # create to object with the defined address
        # p2 = PCA9535_io.PCF(address)
        p2 = IOZero32(address)  # use address 0x21
        # All pins are set to input at start -> set them to output and low
        p2.set_port_direction(0, 0x00)
        p2.set_port_direction(1, 0x00)
        p2.write_port(0, 0x00)
        p2.write_port(1, 0x00)
        pass
    except:
        p2 = None
        logging.info("Error. Could not activate PCA9535_2 on I2C address {}".format(address))
        pass


# check if PCF address parameter is included in settings. Add it to settings if it not already included.
# call PCFActor_1 function once at startup to create the PCF Actor object
class PCA9535_1(CBPiExtension):
    def __init__(self, cbpi):
        self.cbpi = cbpi
        self._task = asyncio.create_task(self.init_actor())

    async def init_actor(self):
        await self.PCA9535_Address_1()
        logger.info("Checked PCF Address")
        PCA9535_Address_1 = self.cbpi.config.get("PCA9535_Address_1", "0x20")
        address = int(PCA9535_Address_1, 16)
        PCFActor_1(address)

    async def PCA9535_Address_1(self):
        global PCA9535_Address_1
        PCA9535_Address_1 = self.cbpi.config.get("PCA9535_Address_1", None)
        if PCA9535_Address_1 is None:
            logger.info("INIT PCA9535_Address_1")
            try:
                await self.cbpi.config.add('PCA9535_Address_1', '0x20', ConfigType.STRING,
                                           'PCA9535_1 I2C Bus address (e.g. 0x20). Change requires reboot')
                PCA9535_Address_1 = self.cbpi.config.get("PCA9535_Address_1", None)
            except:
                logger.warning('Unable to update database')


class PCA9535_2(CBPiExtension):
    def __init__(self, cbpi):
        self.cbpi = cbpi
        self._task = asyncio.create_task(self.init_actor())

    async def init_actor(self):
        await self.PCA9535_Address_2()
        logger.info("Checked PCF Address")
        PCA9535_Address_2 = self.cbpi.config.get("PCA9535_Address_2", "0x21")
        address = int(PCA9535_Address_2, 16)
        PCFActor_2(address)

    async def PCA9535_Address_2(self):
        global PCA9535_Address_2
        PCA9535_Address_2 = self.cbpi.config.get("PCA9535_Address_2", None)
        if PCA9535_Address_2 is None:
            logger.info("INIT PCA9535_Address_2")
            try:
                await self.cbpi.config.add('PCA9535_Address_2', '0x21', ConfigType.STRING,
                                           'PCA9535_2 I2C Bus address (e.g. 0x21). Change requires reboot')
                PCA9535_Address_2 = self.cbpi.config.get("PCA9535_Address_2", None)
            except:
                logger.warning('Unable to update database')


@parameters([Property.Select(label="GPIO", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]),
             Property.Select(label="Inverted", options=["Yes", "No"],
                             description="No: Active on high; Yes: Active on low"),
             Property.Select(label="SamplingTime", options=[2, 5],
                             description="Time in seconds for power base interval (Default:5)")])
class PCA9535Actor_1(CBPiActor):
    # Custom property which can be configured by the user
    @action("Set Power",
            parameters=[Property.Number(label="Power", configurable=True, description="Power Setting [0-100]")])
    async def setpower(self, Power=100, **kwargs):
        self.power = int(Power)
        if self.power < 0:
            self.power = 0
        if self.power > 100:
            self.power = 100
        await self.set_power(self.power)

    async def on_start(self):
        self.power = None
        self.inverted = True if self.props.get("Inverted", "No") == "Yes" else False
        self.p1off = 0 if self.inverted == False else 1
        self.p1on = 1 if self.inverted == False else 0
        self.gpio = self.props.get("GPIO", 1)
        self.sampleTime = int(self.props.get("SamplingTime", 5))
        # p1.pin_mode(self.gpio,"OUTPUT")
        p1.write_pin(self.gpio, self.p1off)
        self.state = False

    async def on(self, power=None):
        if power is not None:
            self.power = power
        else:
            self.power = 100
        await self.set_power(self.power)

        logger.info("ACTOR %s ON - GPIO %s " % (self.id, self.gpio))
        p1.write_pin(self.gpio, self.p1on)
        self.state = True

    async def off(self):
        logger.info("ACTOR %s OFF - GPIO %s " % (self.id, self.gpio))
        p1.write_pin(self.gpio, self.p1off)
        self.state = False

    def get_state(self):
        return self.state

    async def run(self):
        while self.running == True:
            if self.state == True:
                heating_time = self.sampleTime * (self.power / 100)
                wait_time = self.sampleTime - heating_time
                if heating_time > 0:
                    # logging.info("Heating Time: {}".format(heating_time))
                    p1.write_pin(self.gpio, self.p1on)
                    await asyncio.sleep(heating_time)
                if wait_time > 0:
                    # logging.info("Wait Time: {}".format(wait_time))
                    p1.write_pin(self.gpio, self.p1off)
                    await asyncio.sleep(wait_time)
            else:
                await asyncio.sleep(1)

    async def set_power(self, power):
        self.power = power
        await self.cbpi.actor.actor_update(self.id, power)
        pass

@parameters([Property.Select(label="GPIO", options=[17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]),
             Property.Select(label="Inverted", options=["Yes", "No"],
                             description="No: Active on high; Yes: Active on low"),
             Property.Select(label="SamplingTime", options=[2, 5],
                             description="Time in seconds for power base interval (Default:5)")])
class PCA9535Actor_2(CBPiActor):
    # Custom property which can be configured by the user
    @action("Set Power",
            parameters=[Property.Number(label="Power", configurable=True, description="Power Setting [0-100]")])
    async def setpower(self, Power=100, **kwargs):
        self.power = int(Power)
        if self.power < 0:
            self.power = 0
        if self.power > 100:
            self.power = 100
        await self.set_power(self.power)

    async def on_start(self):
        self.power = None
        self.inverted = True if self.props.get("Inverted", "No") == "Yes" else False
        self.p2off = 0 if self.inverted == False else 1
        self.p2on = 1 if self.inverted == False else 0
        self.gpio = self.props.get("GPIO", 1)
        self.sampleTime = int(self.props.get("SamplingTime", 5))
        # p2.pin_mode(self.gpio,"OUTPUT")
        p2.write_pin(self.gpio, self.p2off)
        self.state = False

    async def on(self, power=None):
        if power is not None:
            self.power = power
        else:
            self.power = 100
        await self.set_power(self.power)

        logger.info("ACTOR %s ON - GPIO %s " % (self.id, self.gpio))
        p2.write_pin(self.gpio, self.p2on)
        self.state = True

    async def off(self):
        logger.info("ACTOR %s OFF - GPIO %s " % (self.id, self.gpio))
        p2.write_pin(self.gpio, self.p2off)
        self.state = False

    def get_state(self):
        return self.state

    async def run(self):
        while self.running == True:
            if self.state == True:
                heating_time = self.sampleTime * (self.power / 100)
                wait_time = self.sampleTime - heating_time
                if heating_time > 0:
                    # logging.info("Heating Time: {}".format(heating_time))
                    p2.write_pin(self.gpio, self.p2on)
                    await asyncio.sleep(heating_time)
                if wait_time > 0:
                    # logging.info("Wait Time: {}".format(wait_time))
                    p2.write_pin(self.gpio, self.p2off)
                    await asyncio.sleep(wait_time)
            else:
                await asyncio.sleep(1)

    async def set_power(self, power):
        self.power = power
        await self.cbpi.actor.actor_update(self.id, power)
        pass


def setup(cbpi):
    cbpi.plugin.register("PCA9535Actor_1", PCA9535Actor_1)
    cbpi.plugin.register("PCA9535_Config_1", PCA9535_1)
    cbpi.plugin.register("PCA9535Actor_2", PCA9535Actor_2)
    cbpi.plugin.register("PCA9535_Config_2", PCA9535_2)
    pass
