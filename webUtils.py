'''
Minor tasks relating to the websocket handling
Copyright (C) 2020  TrainLink Organisation (matt-hu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
'''

def obtainAddress(cabAddress, cabID):
    try:
        address = int(cabAddress)
        address = cabAddress
    except ValueError:
        try:
            address = cabID[cabAddress]
        except KeyError:
            print("Bad key")
    return address
