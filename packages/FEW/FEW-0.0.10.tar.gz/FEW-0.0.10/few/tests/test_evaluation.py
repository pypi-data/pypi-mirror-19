"""
Copyright 2016 William La Cava

This file is part of the FEW library.

The FEW library is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

The FEW library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
the FEW library. If not, see http://www.gnu.org/licenses/.

"""
# unit tests for evaluation methods.
from few import FEW
from few.evaluation import *
from few.population import *
from sklearn.datasets import load_boston
import numpy as np
def test_out_shapes():
    """test_evaluation.py: program output is correct size """
    # load test data set
    boston = load_boston()
    # boston.data = boston.data[::10]
    # boston.target = boston.target[::10]
    n_features = boston.data.shape[1]
    # function set

    # terminal set
    term_set = []
    # numbers represent column indices of features
    for i in np.arange(n_features):
        term_set.append({'name':'x','arity':0,'loc':i,'out_type':'f','in_type':None}) # features
        # term_set.append(('k',0,np.random.rand())) # ephemeral random constants

    # initialize population
    pop_size = 5;
    few = FEW(population_size=pop_size,seed_with_ml=False)
    few.term_set = term_set
    pop = few.init_pop(n_features)

    pop.X = np.asarray(list(map(lambda I: out(I,boston.data), pop.individuals)))

    #pop.X = out(pop.individuals[0],boston.data,boston.target)
    print("pop.X.shape:",pop.X.shape)
    print("boston.target.shape",boston.target.shape)
    assert pop.X.shape == (pop_size, boston.target.shape[0])

def test_out_is_correct():
    """test_evaluation.py: output matches known function outputs """

    boston = load_boston()
    n_features = boston.data.shape[1]
    X = boston.data
    Y = boston.target
    p1 = Ind()
    p2 = Ind()
    p3 = Ind()
    p4 = Ind()
    p5 = Ind()
    p1.stack = [{'name':'x', 'arity':0, 'loc':4,'in_type':None,'out_type':'f'},
                {'name':'x','arity':0,'loc':5,'in_type':None,'out_type':'f'},
                {'name':'-','arity':2,'in_type':'f','out_type':'f'},
                {'name':'k', 'arity':0, 'value':.175,'in_type':None,'out_type':'f'},
                {'name':'log','arity':1,'in_type':'f','out_type':'f'},
                {'name':'-','arity':2,'in_type':'f','out_type':'f'}
                ]

    p2.stack = [{'name':'x','arity':0,'loc':7,'in_type':None,'out_type':'f'},
                {'name':'x','arity':0,'loc':8,'in_type':None,'out_type':'f'},
                {'name':'*','arity':2,'in_type':'f','out_type':'f'}
                ]

    p3.stack =  [{'name':'x','arity':0,'loc':0,'in_type':None,'out_type':'f'},
                 {'name':'exp','arity':1,'in_type':'f','out_type':'f'},
                 {'name':'x','arity':0,'loc':5,'in_type':None,'out_type':'f'},
                 {'name':'x','arity':0,'loc':7,'in_type':None,'out_type':'f'},
                 {'name':'*','arity':2,'in_type':'f','out_type':'f'},
                 {'name':'/','arity':2,'in_type':'f','out_type':'f'}
                 ]
    p4.stack =  [{'name':'x', 'arity':0, 'loc':12,'in_type':None,'out_type':'f'},
                 {'name':'sin','arity':1,'in_type':'f','out_type':'f'}
                 ]
    p5.stack = [{'name':'k', 'arity':0, 'value':178.3,'in_type':None,'out_type':'f'},
                {'name':'x','arity':0,'loc':8,'in_type':None,'out_type':'f'},
                {'name':'*','arity':2,'in_type':'f','out_type':'f'},
                {'name':'x','arity':0,'loc':7,'in_type':None,'out_type':'f'},
                {'name':'cos','arity':1,'in_type':'f','out_type':'f'},
                {'name':'+','arity':2,'in_type':'f','out_type':'f'}
                ]

    y1 = safe(np.log(0.175) - (X[:,5] - X[:,4]))
    y2 = safe(X[:,7]*X[:,8])
    y3 = safe(divs(X[:,5]*X[:,7],np.exp(X[:,0])))
    y4 = safe(np.sin(X[:,12]))
    y5 = safe(178.3*X[:,8]+np.cos(X[:,7]))

    # y1,y2,y3,y4,y5 = safe(y1),safe(y2),safe(y3),safe(y4),safe(y5)

    assert np.array_equal(y1,out(p1,X))
    print("y1 passed")
    assert np.array_equal(y2,out(p2,X))
    print("y2 passed")
    assert np.array_equal(y3, out(p3,X))
    print("y3 passed")
    # print("y4:",y4,"y4hat:",out(p4,X,Y))
    assert np.array_equal(y4, out(p4,X))
    print("y4 passed")
    assert np.array_equal(y5, out(p5,X))

def test_calc_fitness_shape():
    """test_evaluation.py: calc_fitness correct shapes """
    # load test data set
    boston = load_boston()
    # boston.data = boston.data[::10]
    # boston.target = boston.target[::10]
    n_features = boston.data.shape[1]
    # terminal set
    term_set = []
    # numbers represent column indices of features
    for i in np.arange(n_features):
        term_set.append({'name':'x','arity':0,'loc':i,'out_type':'f','in_type':None}) # features
        # term_set.append(('k',0,np.random.rand())) # ephemeral random constants

    # initialize population
    pop_size = 5;
    few = FEW(population_size=pop_size,seed_with_ml=False)
    few.term_set = term_set
    pop = few.init_pop(n_features)

    pop.X = np.asarray(list(map(lambda I: out(I,boston.data), pop.individuals)))

    fitnesses = calc_fitness(pop.X,boston.target,'mse')
    assert len(fitnesses) == len(pop.individuals)

    # test vectorized fitnesses
    vec_fitnesses = calc_fitness(pop.X,boston.target,'mse_vec')
    fitmat = np.asarray(vec_fitnesses)
    print("fitmat.shape:",fitmat.shape)
    assert fitmat.shape == (len(pop.individuals),boston.target.shape[0])
