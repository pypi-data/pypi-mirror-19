#IOT:1

My custom protocol for communication between devices at home. 
It uses UPD and broadcast. 
Messages are json strings.

## Message body:

    {
        "protocol": "iot:1",
        "node": "Rpi-lcd-1",
        "chip_id": "RpiB",
        "event": "lcd.content",
        "parameters: [
            "content": "-(=^.^)"
        ],
        "response": '',
        "targets": [
            "nodemcu-lcd-40x4"
        ]
    }

- protocol: defines name, currently iot:1
- node: friendly node name like light-room-big or screen-one-kitchen
- chip_id: a unique device id
- event: event name like light.on or dispay
- parameters: array of parameters. like rows to display
- response: used when responding to request, ie returning toilet state
- targets: message targets by nde name. special keyword ALL for all nodes in network

## functions

### Message(node, chip_id=None)

Create instance of class. Node is a node name, chip_id if blank will be generated

### prepare_message(data=None)

Returns empty message dictionary. If data is passed it copy values from it.

### decode_message(string)

Decode json string to dict message. Validates protocol and targets.
 Return None on failure



