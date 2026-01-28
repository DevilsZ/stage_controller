# stage_controller
GUI soft for SIGMA-KOKI SHOT-204

Function of Each Switch
- connect: Connects to the device. Note the COM port.
- origin: Home position return command.
- move(rel): Moves to a relative position. Should move in the opposite direction with negative values, but doesn't work.
- move(abs): Moves to an absolute position. Should move in the opposite direction with negative values, but doesn't work.
- speed: Speed settings box. From left: minimum speed, maximum speed, acceleration/deceleration time. However, changing these values doesn't seem to significantly alter the speed.
- jog: Manual operation. Moves only while pressed? Plus/minus possible
- stop: Stop command
- position: Should display current axis position, but doesn't work
- exit: Program exit

Current Issues
- Move doesn't move in negative direction
- Unclear how to set speed → Resolved?
- Currently inputting in pulse units, but should be possible to change to µm units by adjusting open/close. However, adjusting causes it to stop moving entirely
- Are memory switch settings shared between manual and PC control??
- Jog tends to freeze
- Position displays nothing → Resolved
- Mysterious error sound and motor noise present, but it doesn't move
