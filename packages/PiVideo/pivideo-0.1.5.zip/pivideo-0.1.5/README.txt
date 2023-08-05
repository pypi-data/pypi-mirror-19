PiVideo Control Software
The PiVideo software may be used to control the PiCapture processor.  Some of the functions provided by this software include:
-	Automatic or manual video source selection 
-	Optional on-screen source indication
-	Test mode control
-	A firmware update utility
By default, the PiVideo software communicates with the PiCapture processor using the Raspberry Pi i2c port 1.  If you are using this port for other applications,  jumpers may be used to select one of the two I2C ports as an alternative.  The default I2C address is 0x40, and the PiCapture can operate with other I2C slave devices attached to the port.  The serial port is required to perform software updates.

pivideo_class is provided for use with your own programs.

Please see lintestsystems.com for additional documentation.

Changelog:

1.2 	First public release
1.3 	Changes to serial port handling to support Raspberry Pi 3
1.4	Fixed -v parameter processing bug
1.5	Added support for PiCapture HD1
