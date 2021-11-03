from hat.drivers import iec104
import sys
import asyncio

class DeviceCommunication:
    def __init__(self, processing):
        self._connection = None
        self._processing = processing
    
    async def connect(self):
        self._connection = await iec104.connect(iec104.Address("127.0.0.1", 9999))
    
    async def receive_loop(self):
        state = {'i1': 0, 'i2': 0, 'i3':0, 'i4':0}
        while True:
            protocol_data = await connection.receive()
            processing.on_receive(protocol_data)
            
class Processing:
    def __init__(self, hmi):
        self._state = {'i1': 0, 'i2': 0, 'i3':0, 'i4':0}
        self._hmi = hmi
        
    
    def on_receive(self, protocol_data):
        value = round(protocol_data[0].value.value, 2)
        address = protocol_data[0].asdu_address
        asdu_to_current = {0: 'i1', 1: 'i2', 2: 'i3'}
        key = asdu_to_current[address]
        self._state[key] = value
        self._state['i4'] = round(self._state['i1'] + self._state['i2'] + self._state['i3'], 2)
        self._hmi.render(self._state)

class HumanMachineInterface:

    def render(self, state):
        for key, mesurement in state.items():
            print(key, '=', mesurement)
        print()

async def async_main():
    hmi = HumanMachineInterface()
    processing = Processing(hmi)
    communication = DeviceCommunication(processing)
    await communication.connect()
    await communication.receive_loop()

def main():
    asyncio.run(async_main())

if __name__ == '__main__':
    sys.exit(main())