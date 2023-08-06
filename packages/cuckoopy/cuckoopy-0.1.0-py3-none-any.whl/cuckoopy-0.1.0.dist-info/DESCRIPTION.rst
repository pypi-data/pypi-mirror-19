Copyright (c) 2016 Rajath Agasthya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description: cuckoopy: Pure Python implementation of Cuckoo Filter
        =====================================================
        
        .. image:: https://travis-ci.org/rajathagasthya/cuckoopy.svg?branch=master
            :target: https://travis-ci.org/rajathagasthya/cuckoopy
        
        
        Cuckoo Filter, like Bloom Filter, is a probabilistic data structure for fast,
        approximate set membership queries, with some small false positive probability.
        While Bloom Filters are space efficient and are widely used, they do not
        support deletion of items from the set without rebuilding the entire filter.
        This can be overcome with several extensions to Bloom Filters such as
        Counting Bloom Filters, but with significant space overhead.
        
        Cuckoo Filters support adding and removing items dynamically while achieving
        higher performance than Bloom filters. A Cuckoo Filter is based on partial-key
        cuckoo hashing that stores only fingerprint of each item inserted. Cuckoo
        Filters provide higher lookup performance than Bloom Filters and uses less
        space than Bloom Filters if the target false positive rate is < 3%.
        
        The original research paper `Cuckoo Filter: Practically Better Than Bloom
        <https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf>`_ by Bin Fan,
        David G. Andersen, Michael Kaminsky and Michael D. Mitzenmacher
        describes the data structure in more detail.
        
        
        Installation
        ------------
        Make sure you have Python_ (3.5+) installed on your system. If you don't have
        it, follow `these instructions <https://docs.python.org/3/using/index.html>`_
        to install it.
        
        .. _Python: https://www.python.org/
        
        Install cuckoopy using:
        
        .. code-block::
        
            $ pip install cuckoopy
        
        
        Usage
        -----
        .. code-block:: python
        
            >>> from cuckoopy import CuckooFilter
            # Initialize a cuckoo filter with 10000 buckets with bucket size 4 and fingerprint size of 1 byte
            >>> cf = CuckooFilter(capacity=10000, bucket_size=4, fingerprint_size=1)
        
        Insert an item into the filter:
        
        .. code-block:: python
        
            >>> cf.insert('Hello!')
            True
        
        Lookup an item in the filter:
        
        .. code-block:: python
        
            >>> cf.contains('Hello!')
            True
            >>> 'Hello!' in cf
            True
        
        Delete an item from the filter:
        
        .. code-block:: python
        
            >>> cf.delete('Hello!')
            True
        
        Get the size (number of items present) of the filter:
        
        .. code-block:: python
        
            >>> cf.size
            4
            >>> len(cf)
            4
        
        
        Running tests locally
        ---------------------
        This project uses `pytest <http://docs.pytest.org>`_ for tests. Make sure you
        have ``tox`` installed on your local machine and from the root directory of the
        project, run:
        
        .. code-block::
        
            $ tox
        
        This command runs unit tests in python 3.5 and python 3.6 environments with
        code coverage details. It also runs pep8 (flake8) checks. To run tox against a
        specific environment (py35, py36 or pep8), use the ``-e`` option.
        
        
        License
        -------
        `MIT License <https://github.com/rajathagasthya/cuckoopy/blob/master/LICENSE>`_
        
        
        Useful Links
        ------------
        * `Probabilistic Filters By Example <https://bdupras.github.io/filter-tutorial/>`_
        * `Original C++ implementation by the authors of the research paper <https://github.com/efficient/cuckoofilter/>`_
        
Platform: UNKNOWN
Classifier: Development Status :: 3 - Alpha
Classifier: Intended Audience :: Developers
Classifier: Natural Language :: English
Classifier: License :: OSI Approved :: MIT License
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.5
Classifier: Programming Language :: Python :: 3.6
