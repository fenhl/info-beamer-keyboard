#!/usr/bin/env python3

import asyncio
import basedir
import evdev

import info_beamer_keyboard

def dump_state(state):
    with open('node/data.json', 'w') as data_f:
        json.dump(state.to_json(), data_f, indent=4, sort_keys=True)
        print(file=data_f) # add trailing newline

@asyncio.coroutine
def handle_device(device):
    event = yield from device.async_read_one()
    return device, event

@asyncio.coroutine
def handle_events(devices):
    for did, future in devices.items():
        if isinstance(future, tuple):
            devices[did] = asyncio.async(handle_device(future[0]))
    yield from asyncio.wait(devices.values(), return_when=asyncio.FIRST_COMPLETED)
    for did, future in devices.items():
        if future.done():
            devices[did] = future.result()

@asyncio.coroutine
def main():
    layout = info_beamer_keyboard.Layout(basedir.config_dirs('fenhl/keylayout.json').json(readable_only=True))
    state = info_beamer_keyboard.State(layout)
    dump_state(state)
    devices = {
        device_id(device): asyncio.async(handle_device(device))
        for device in [evdev.InputDevice(d) for d in evdev.list_devices('/dev/input/')]
    }
    while True:
        yield from handle_events(devices)
        for did, future in devices.items():
            if not isinstance(future, tuple):
                continue
            device, event = future
            # keyboard input
            if event.type != evdev.ecodes.EV_KEY:
                continue
            state = state.with_event(device, event)
            dump_state(state)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
