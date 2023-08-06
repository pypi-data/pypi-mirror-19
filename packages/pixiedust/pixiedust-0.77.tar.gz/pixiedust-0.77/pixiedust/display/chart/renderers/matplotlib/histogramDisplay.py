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

from pixiedust.display.chart.renderers import PixiedustRenderer
from .matplotlibBaseDisplay import MatplotlibBaseDisplay
import matplotlib.pyplot as plt
import mpld3
import numpy as np
import math
import pixiedust

myLogger = pixiedust.getLogger(__name__)

@PixiedustRenderer(id="histogram")
class HistogramDisplay(MatplotlibBaseDisplay):

    def supportsAggregation(self, handlerId):
        return False

    def supportsLegend(self, handlerId):
        return False

    # TODO: add support for keys
    def supportsKeyFields(self, handlerId):
        return False
    
    def getPreferredDefaultValueFieldCount(self, handlerId):
        return 1

    # no keys by default
    def getDefaultKeyFields(self, handlerId, aggregation):
        return []

    def matplotlibRender(self, fig, ax):
        stacked = len(self.getValueFields()) > 1
        self.getWorkingPandasDataFrame().plot(kind="hist", stacked=stacked, ax=ax)

        # keyFieldValues = self.getKeyFieldValues()
        # valueFields = self.getValueFields()
        # valueFieldValues = self.getValueFieldValueLists()
        # myLogger.info("histogram: {0} \r\n{1} \r\n{2}".format(keyFieldValues, valueFields, valueFieldValues))
        # # TODO: add support for keys
        # numHistograms = max(len(keyFieldValues),1) * len(valueFields)
        # colors = self.colormap(np.linspace(0., 1., numHistograms))
        # if numHistograms > 1:
        #     fig.delaxes(ax)
        #     if numHistograms < 3:
        #         histogramGridPrefix = "1" + str(numHistograms)
        #     else:
        #         histogramGridPrefix = str(int(math.ceil(numHistograms//2))) + "2"
        #     for i, valueField in enumerate(valueFields):
        #         ax2 = fig.add_subplot(histogramGridPrefix + str(i+1))
        #         n, bins, patches = ax2.hist(valueFieldValues[i], 30, histtype='bar', fc=colors[i], alpha=0.5)
        #         for j, patch in enumerate(patches):
        #             self.connectElementInfo(patch, n[j])
        #         ax2.set_xlabel(valueFields[i], fontsize=18)
        # else:
        #     n, bins, patches = ax.hist(valueFieldValues[0], 30, histtype='bar', fc=colors[0], alpha=0.5)
        #     if self.has_mpld3:
        #         for j, patch in enumerate(patches):
        #             self.connectElementInfo(patch, n[j])
        #     ax.set_xlabel(valueFields[0], fontsize=18)