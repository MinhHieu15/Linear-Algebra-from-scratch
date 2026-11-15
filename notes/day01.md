# Day 01 — NumPy basics

**Watched:** BC 05 › 002 Introduction to Numpy, 003 Numpy Arrays

## Key ideas (in my own words)

- np.array() -> 1D Vecto
- np.array([[]]) -> 2D Matrix
- np.array([
    [];
    []
])
-> 3D Shape

-np.reshape(x,y,z) (x:layers, y:rows, z:columns)

- np.arange(x,y,z) (x:start,y:end,z:step)
- np.linspace(x,y,z) (x:start,y:end,z:numbers in vector)

-np.rand(x,y,z) (x:rows,y:columns, z:dimensions) (rand gives random uniform distribution from 0 to 1)
same as np.random.default_rng(0)

-np.randn(x,y,z) (x:rows,y:columns, z:dimensions) (randn gives random normal disibution around 0)
same as np.normal((size = ))

-np.randint(x,y,z) (x:start, y:stop, z:quantity) (randint gives random int number from x to y)
same as np.integers(x,y,z)



-np.zeros(x,y,z) (x:rows, y:columns, z:dimensions) (gives full of zeros)
-np.ones(x,y,z)  (gives full of ones)
-np.eye(x,y,z)   (give a square matrix)


-if you take a part of a vector as a variable, you change the index of that variable, the original vector changes too!

-arr[arr>5] -> return the only index that satisfies the conditions
## Worked examples by hand

## Still unclear

-
