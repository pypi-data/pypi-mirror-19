# spylon-kernel
[![Build Status](https://travis-ci.org/mariusvniekerk/spylon-kernel.svg?branch=master)](https://travis-ci.org/mariusvniekerk/spylon-kernel)
[![codecov](https://codecov.io/gh/mariusvniekerk/spylon-kernel/branch/master/graph/badge.svg)](https://codecov.io/gh/mariusvniekerk/spylon-kernel)

This is an extremely early proof of concept for using the metakernel in combination with py4j to make a simpler
kernel for scala.

## Installation

On python 3.5+

```bash
pip install .
```

## Installing the jupyter kernel

To install the jupyter kernel install it using

```
python -m spylon_kernel install
```

## Using the kernel

The scala spark metakernl prodived a scala kernel by default.
At the first scala cell that is run a spark session will be constructed so that a user can interact with the 
interpreter.

## Customizing the spark context

The launch arguments can be customized using the `%%init_spark` magic as follows

```python
%%init_spark
launcher.jars = ["file://some/jar.jar"]
launcher.master = "local[4]"
launcher.conf.spark.executor.cores = 8
```

## Other languages

Since this makes use of metakernel you can evaluate normal python code using the `%%python` magic.  In addition once 
the spark context has been created the `spark` variable will be added to your python ernvironment.

```python
%%python
df = spark.read.json("examples/src/main/resources/people.json")
```

To get completions for python, make sure that you have installed `jedi`


