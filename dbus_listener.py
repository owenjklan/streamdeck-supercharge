import dbus_next
from dbus_next.message import Message, MessageType
from dbus_next.aio import MessageBus

import asyncio
import json

loop = asyncio.new_event_loop()


async def main():
    bus = await MessageBus(bus_type=dbus_next.BusType.SESSION).connect()

    reply = await bus.call(
        Message(destination='org.gnome.Shell.Introspect',
                path='/org/gnome/Shell/Introspect',
                interface='org.gnome.Shell.Introspect',
                member='GetRunningApplications'))

    if reply.message_type == MessageType.ERROR:
        print(json.dumps(reply.body, indent=4, default=str))
        raise Exception(reply.body[0])

    print(json.dumps(reply.body[0], indent=2))


loop.run_until_complete(main())