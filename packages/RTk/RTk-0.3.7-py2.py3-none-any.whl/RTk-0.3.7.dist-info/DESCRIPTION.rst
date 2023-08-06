RTk Python Library
=====

This library contains 2 main modules. GPIO and smbus.

The RTk.GPIO Library aims to replicate most functions found in the RPi.GPIO Library. You should be able to use existing code and tutorials by changing "RPi.GPIO" to "RTk.GPIO".
You can also import it using either "from RTk import GPIO" or "import RTk.GPIO as GPIO" like you can with RPi.GPIO.

The RTk.smbus library aims to replicate the python-smbus library used to access I2C devices on the Raspberry Pi. You can import it by importing "RTk.smbus".

Documentation can be found on our wiki on how to use these.

License
=====

This code is distributed under the GNU GPL V3 license and is Copyright Ryanteck LTD. 2016.

In short the GNU GPL V3 License allows modification, distribution, commerical use, and more as long as the source code and any changes are re-distributed.
However there is no warranty provided with this software.

The full license can be found in the License file. 

GPIO Library originally based on AnyIO by David Whale (@whaleygeek) which is licensed under the MIT license and can be found at https://github.com/whaleygeek/anyio. Big thank you for the basis of this software.

This library requires pyserial and other python libraries to work. These are distributed under their own licenses.



