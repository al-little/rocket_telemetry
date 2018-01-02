import Controller

controller = Controller.Controller()

controller.run()

while True:
    # ctrl-c to quit
    cmd = input('telemetry cmd$ ')

    controller.commands.append(cmd)

    print('execute: ' + cmd)
