# -*- coding: utf-8 -*-
# This file automatically created while building Larch. Do not edit manually.
configuration='DEFAULT'
time='11:49:35 AM Central Standard Time'
date='12 Jan 2017'
day='Thursday'
ymdh='2017011211'[3:]
from . import __version__ as version
import sys

build='%s (%s, %s %s)'%(version,day,date,time)
longversion='%s.%s%s'%(version,ymdh,sys.platform[0])
from .apsw import apswversion, sqlitelibversion
from .util import dicta
versions = dicta({
'larch':version,
'apsw':apswversion(),
'sqlite':sqlitelibversion(),
})

try:
	import numpy
	versions['numpy'] = numpy.version.version
except:
	versions['numpy'] = 'failed'

try:
	import scipy
	versions['scipy'] = scipy.version.version
except:
	versions['scipy'] = 'failed'

try:
	import pandas
	versions['pandas'] = pandas.__version__
except:
	versions['pandas'] = 'failed'

import sys
versions['python'] = "{0}.{1}.{2} {3}".format(*(sys.version_info))
build_config='Larch %s built on %s, %s %s'%(configuration,day,date,time)
