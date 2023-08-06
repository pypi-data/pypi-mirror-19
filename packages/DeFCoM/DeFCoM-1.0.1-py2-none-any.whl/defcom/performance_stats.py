#---------------------------------------------------------------------
# DeFCoM: A supervised learning genomic footprinter
# Copyright (C) 2016  Bryan Quach
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#----------------------------------------------------------------------

import uuid
import subprocess
from numpy import concatenate
from sklearn.metrics import roc_curve, auc

"""Methods for computing performance statistics."""

def pAUC(y_true, y_score, fpr_cutoff):
    """ Calculate partial Area Under ROC (pAUC).

    Computes a pAUC value given a specified false positive rate (FPR) 
    cutoff. It is important to note that the exact pAUC cannot be computed.
    The accuracy of the calculation depends on the resolution of data 
    points produced by an intermediary ROC curve. The FPR data point 
    closest to and greater than the cutoff specified will be used for 
    interpolation to determine the pAUC at the specified FPR cutoff. For these
    FPR values, the highest associated TPR values are used.

    Args:
        y_true: Array-like of true binary class labels in range {0, 1} or 
            {-1, 1} corresponding to y_score. The larger value represents 
            the positive class.

        y_score: Array-like of target scores with higher scores indicating
            more confidence in the positive class.

        fpr_cutoff: A float specifying the FPR cutoff to use in computing 
            the pAUC. Must be in the interval (0,1).

    Returns:
        A float representing the pAUC value.

    Raises:
        AssertionError: The FPR cutoff is not in the interval (0,1)
    """
    error_msg = "FPR cutoff must be in (0,1)"
    assert fpr_cutoff > 0.0 and fpr_cutoff < 1.0
    fpr, tpr, trash = roc_curve(y_true, y_score, drop_intermediate=False)
    index_low = len([1 for i in fpr if i < fpr_cutoff])-1
    index_high = index_low + 1
    #Get interpolated TPR value from FPR cutoff
    if index_low == -1:  #No ROC data points lower than cutoff
        x0 = fpr[0]
        try:
            x1 = min([xv for (c,xv) in zip([x>x0 for x in fpr],fpr) if c])
        except ValueError:
            x1 = x0
        y0 = max([yv for (c,xv,yv) in zip([x==x0 for x in  fpr],fpr,tpr) if c])
        y1 = max([yv for (c,xv,yv) in zip([x==x1 for x in  fpr],fpr,tpr) if c])
        #Apply line derived from two closest points from FPR cutoff
        tpr_cutoff = fpr_cutoff*((y1-y0)/(x1-x0)) + ((x1*y0-x0*y1)/(x1-x0))
        #Segment full ROC to get partial ROC
        fpr = [0.0] + [fpr_cutoff]
        tpr = [0.0] + [tpr_cutoff]
    elif index_high == len(fpr):  #No ROC data points higher than cutoff
        try:
            x0 = max([xv for (c,xv) in zip([x<x1 for x in fpr],fpr) if c])
        except ValueError:
            x0 = x1
        x1 = fpr[index_high-1]
        y0 = max([yv for (c,xv,yv) in zip([x==x0 for x in  fpr],fpr,tpr) if c])
        y1 = max([yv for (c,xv,yv) in zip([x==x1 for x in  fpr],fpr,tpr) if c])
        #Apply line derived from two closest points from FPR cutoff
        tpr_cutoff = fpr_cutoff*((y1-y0)/(x1-x0)) + ((x1*y0-x0*y1)/(x1-x0))
        #Segment full ROC to get partial ROC
        fpr = concatenate((fpr,[fpr_cutoff]), axis=0)
        tpr = concatenate((tpr, [tpr_cutoff]), axis=0)
    else:
        x0 = fpr[index_low]
        x1 = fpr[index_high]
        y0 = max([yv for (c,xv,yv) in zip([x==x0 for x in  fpr],fpr,tpr) if c])
        y1 = max([yv for (c,xv,yv) in zip([x==x1 for x in  fpr],fpr,tpr) if c])
        #Apply line derived from two closest points from FPR cutoff
        tpr_cutoff = fpr_cutoff*((y1-y0)/(x1-x0)) + ((x1*y0-x0*y1)/(x1-x0))
        #Segment full ROC to get partial ROC
        fpr = concatenate((fpr[:index_high], [fpr_cutoff]), axis=0)
        tpr = concatenate((tpr[:index_high], [tpr_cutoff]), axis=0)
    return auc(fpr,tpr)/fpr_cutoff

