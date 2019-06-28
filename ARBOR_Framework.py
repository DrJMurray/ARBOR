
# coding: utf-8

# In[9]:

# We begin by defining a simple Tree class, which will be useful later on
# together with some functions for simulating random 'tree' measurements
import numpy as np
import math as math
from scipy.spatial import distance
import random
from scipy.stats import norm
import math
import csv
import scipy
from scipy.stats import norm
from scipy.optimize import linear_sum_assignment as hungarian

import json

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from scipy import stats
from sklearn.metrics import mean_squared_error
from math import sqrt


# In[28]:

#used in guassian curve generation
def adjustCurveToHeight(new_max, datas):
    maxVal = np.max(datas)
    if maxVal == 0:
        return datas + new_max
    ratio = new_max/(float(maxVal))
    return datas * ratio



#our tree model
class Tree(object):
    """ Tree object with height / canopy size / position """

    def __init__(self, x, y, height, area,id):
        self.id = id
        self.x = x
        self.y = y
        self.h = height
        self.a = area

    def data(self):
        return "x:{},y:{},h:{},a:{},".format(self.x,self.y,self.h,self.a)

    def getRadius(self):
        return math.sqrt(float(self.a)/float(np.pi))

    #reverses the diff score
    def cost(self,other):
        return 1.0 - self.diff(other)

    #diff using guassian method, 0 to 1.
    def diff(self, other):

        try:
            #how far apart are these things? turn it into a 1D problem..
            distance = math.hypot(other.x - self.x, other.y - self.y)
            full_distance = distance + (max(other.getRadius(),self.getRadius())*4)
            x = np.linspace(-(full_distance/2.0),(full_distance/2.0),1000)

            #generate some curves for each tree
            initial_tree_curve_a = mlab.normpdf(x, -distance/2.0, self.getRadius())
            initial_tree_curve_b = mlab.normpdf(x, distance/2.0, other.getRadius())

            #adjust to the correct height
            curve1data = adjustCurveToHeight(self.h,initial_tree_curve_a)
            curve2data = adjustCurveToHeight(other.h,initial_tree_curve_b)

            #this gets the minimum of either (essentiully the Intersect)
            minimum=np.minimum(curve1data,curve2data)

            #this gets the maximum of either (essentiully the Union)
            maximum=np.maximum(curve1data,curve2data)

            #calulate the jaccard of the overlapping area.
            area_under_1 = float(np.trapz(curve1data, x=x))
            area_under_2 = float(np.trapz(curve2data, x=x))
            overlap_area = float(np.trapz(minimum, x=x))
            union_area = float(np.trapz(maximum, x=x))

            #if they dont overlap at all return 0 ( a complete mismatch)
            #this would normally be impossible but we have trimmed the tails of the curves
            #therefore a complete mismatch is possible when no overlap.
            if union_area == 0:
                print "Union area 0"
                return 0

            #return the overlap. 1 = a complete overlap!
            return float(overlap_area / union_area)

        except Exception:
            print(self.data())
            print(other.data())
            return 0


# In[36]:

#functions

#this should load the trees from a csv in a format of ID,X,Y,HS,AS
def load_trees_from_CSV(filename):
    ids = [] #load xs
    ground_xs = [] #load xs
    ground_ys = [] #load ys
    ground_hs = [] #load heights
    ground_as = [] #load areas

    f = open(filename,'rU')
    csv_f = csv.reader(f)

    count = 0;
    for row in csv_f:
        if len(row)is 4:
            row.insert(0, count)
        try:
            #if anything is 0 we should ignore it - it is an impossible tree..
            asfloats = [float(row[1]),float(row[2]),float(row[3]), float(row[4])];
            if 0 not in asfloats and not np.isnan(asfloats).any():
                ids.append(float(row[0]))
                ground_xs.append(float(row[1]))
                ground_ys.append(float(row[2]))
                ground_hs.append(float(row[3]))
                ground_as.append(float(row[4]))
            else:
                print "skipping as non-real tree (dimensions are 0) detected."
        except ValueError as e:
            print e
        count = count+1
    trees = [Tree(x, y, h, a, tid) for x, y, h, a, tid in zip(ground_xs, ground_ys, ground_hs, ground_as, ids)]
    return trees


#runs hungarian matching
def gen_assignment_hungarian(trees_a, trees_b):
    cost = np.array([[tree_b.cost(tree_a) for tree_b in trees_b] for tree_a in trees_a])
    row_ind, col_ind = hungarian(cost)
    pairs = [(trees_a[r], trees_b[c]) for r, c in zip(row_ind, col_ind)]
    return pairs


#generates the average difference between the two sets of trees.
def genScore(pairs):
    if len(pairs) is 0:
        return None
    score = 0
    for (a,b) in pairs:
        score += a.diff(b)
    return score/float(len(pairs))


#which one if these is correct?
def genIDXDSS(treesa, treesb, pairs):
    minimum=min(len(treesa),len(treesb))
    maximum=max(len(treesa),len(treesb))
    if float(len(pairs))/float(minimum) > 1.0:
        print('Something went wrong {} {} {}'.format(len(treesa), len(treesb),len(pairs)))
    return float((minimum))/float(maximum)



# In[37]:

#now test with some examples
trees1 = load_trees_from_CSV('ARBOR_TestData.csv')
trees2 = load_trees_from_CSV('ARBOR_TestData1.csv')
trees3 = load_trees_from_CSV('ARBOR_TestData2.csv')

pairs = gen_assignment_hungarian(trees1, trees2)
amps_score = genScore(pairs)
dss_score = genIDXDSS(trees1,trees2, pairs)

print("set 1 to 2 => AMPS: {}, DSS: {}".format(amps_score, dss_score));

pairs = gen_assignment_hungarian(trees1, trees3)
amps_score = genScore(pairs)
dss_score = genIDXDSS(trees1,trees3, pairs)

print("set 1 to 3 => AMPS: {}, DSS: {}".format(amps_score, dss_score));


# In[ ]:
