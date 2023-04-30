# girgs

![Model](https://github.com/viethan/girgs/blob/main/img/for_readme/image0.png)
![Model](https://github.com/viethan/girgs/blob/main/img/for_readme/image1.png)

The development of this project has influenced by the 2017 paper "Sampling Geometric Inhomogeneous Random Graphs in Linear Time", by Karl Bringmann, Ralph Keusch and Johannes Lengler.

Click [here](https://arxiv.org/abs/1511.00576) for the arXiv page.

## Creating the environment

Notes:
  1. we use python version 3.10 because Cython exhibits some issues with the latest version
  2. we use NetworkX in order to sample values from a power law distribution

```bash
conda create --name env_name -c conda-forge graph-tool python=3.10
conda activate env_name
pip install Cython networkx[default]
```

Navigate to girgs/

```bash
python setup.py build_ext --inplace
```

## Project Structure

```bash
girgs
├── experiments
│   ├── custom.py
│   └── SIR_eventdriven.py
├── img
│   ├── n10000_alpha8_beta2.8_wmin1.pdf
│   ├── n10000_alpha8_beta2.8_wmin3.pdf
│   ├── n1000_alpha2.5_beta2.2_wmin3.pdf
│   ├── n1000_alpha2.5_beta2.8_wmin3.pdf
│   ├── n1000_alpha8_beta2.2_wmin3.pdf
│   ├── n1000_alpha8_beta2.8_wmin3.pdf
│   ├── test_clusteringcoeff_output.png
│   └── test_scalefree_output.png
├── README.md
├── setup.py
├── src
│   ├── dnu.pyx
│   ├── girg.pyx
│   ├── __init__.py
│   ├── pnu.py
│   └── weightlayers.py
└── test
    ├── test_clusteringcoeff.py
    ├── test_dnu.py
    ├── test_pnu.py
    └── test_scalefree.py
 ```
 
1. src/

  - contains all of the files that make up the sampler

2. test/

  - `test_dnu.py` tests the data structure from Lemma 4.1.
  - `test_pnu.py` tests the data structure from Lemma 4.2.
  - `test_scalefree.py` checks if the degree distribution follows a power law
  - `test_clusteringcoeff.py` checks the clustering coeffs of a number of graphs with varying parameters

3. experiment/

  - `custom.py` samples a girg.
  - `SIR_eventdriven.py` simulates a continuous-time SIR epidemic using an event-driven algorithm

 4. img/

  - contains the visualisations of multiple experiments
  - contains the output of `test_scalefree.py` and `test_clusteringcoeff.py`.

  Important notes:
   - the visualisations are of graphs in 2D
    
   - the papers specifies that the ground space used is a torus, meaning that it is possible to wrap around. In order to not make our visualisations messy, we slightly altered `girg.pyx` in order to provide clearer representations
    

```python
@cython.boundscheck(False)
cdef long double dist_torus_points(np.ndarray[np.float64_t, ndim=1] x_u, np.ndarray[np.float64_t, ndim=1] x_v, int d):
    cdef long double maximum, dist
    maximum = 0.0

    for i in range(d):
        # original - dist = min(abs(x_u[i] - x_v[i]), 1 - abs(x_u[i] - x_v[i]))
        dist = abs(x_u[i] - x_v[i])
        maximum = max(maximum, dist)

    return maximum
```
 

## Performance 

Here are some preliminary results. 

Note that we performed these experiments with alpha=8, beta=2.8, d=2, c=2 and a varying number of vertices.

* 10,000 vertices - 12 seconds
* 100,000 vertices - 115 seconds
* 500,000 vertices - 667 seconds
