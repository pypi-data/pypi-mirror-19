# -------------------------------------------------------------------------------
# Copyright IBM Corp. 2016
# 
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------------

import os
from . import storage
import pkg_resources
import binascii
import shutil
from . import pdLogging

storage._initStorage();

#Misc helper methods
def fqName(entity):
    return (entity.__module__ + "." if hasattr(entity, "__module__") else "") + entity.__class__.__name__

#init scala bridge, make sure that correct pixiedust.jar is installed

jarDirPath = os.environ.get("PIXIEDUST_HOME", os.path.expanduser('~')) + "/data/libs/"
jarFilePath = jarDirPath + "pixiedust.jar"

dir = os.path.dirname(jarDirPath)
if not os.path.exists(dir):
    os.makedirs(dir)

def installPixiedustJar():
    with pkg_resources.resource_stream(__name__, "resources/pixiedust.jar") as resJar:
        with open( jarFilePath, 'wb+' ) as installedJar:
            shutil.copyfileobj(resJar, installedJar)
            print("Pixiedust runtime updated. Please restart kernel")

copyFile = True
if os.path.isfile(jarFilePath):
    with open( jarFilePath, 'rb' ) as installedJar:
        installedCRC = binascii.crc32( installedJar.read() )
        with pkg_resources.resource_stream(__name__, "resources/pixiedust.jar") as resJar:
            copyFile = installedCRC != binascii.crc32( resJar.read() )

if copyFile:
    installPixiedustJar()

"""
Helper decorator that automatically cache results of a class method into a field
"""
from . import pdLogging
myLogger = pdLogging.getLogger(__name__)
def cache(fieldName):
    def outer(func):
        def inner(cls, *args, **kwargs):
            if hasattr(cls, fieldName) and getattr(cls, fieldName) is not None:
                myLogger.debug("Found Cache!!! {0}".format(fieldName))
                return getattr(cls, fieldName)
            retValue = func(cls, *args, **kwargs)
            setattr(cls, fieldName, retValue)
            return retValue
        return inner
    return outer
