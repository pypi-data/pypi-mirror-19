Copyright (c) 2015 Aaron Halfaker

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

Description: # MediaWiki database
        
        This library provides a set of utilities for connecting to and querying a
        MediaWiki database.  
        
        * **Installation:** ``pip install mwdb``
        * **Documentation:** https://pythonhosted.org/mwdb
        * **Repositiory:** https://github.com/mediawiki-utilities/python-mwdb
        * **License:** MIT
        
        The `Schema()` object is a thin wrapper around a
        sqlalchemy `Engine` and `Meta` adapts to the local database setup.  When using
        `Schema()` member table ORM, the internal mapping will translate between
        public replicas views (e.g. ``revision_userindex``, ``logging_userindex`` and
        ``logging_logindex``) transparently.  This allows you to write one query that
        will run as expected on either schema.
        
        At the moment, the `execute()` method does not make any such conversion, but a
        helper attribute `public_replica` that is `True` when querying a views via
        public replica and `False` when querying the production database.
        
        ## Example
        
            >>> import mwdb
            >>> enwiki = mwdb.Schema("mysql+pymysql://enwiki.labsdb/enwiki_p" +
            ...                      "?read_default_file=~/replica.my.cnf")
            >>> enwiki.public_replica
            True
            >>>
            >>> with enwiki.transaction() as session:
            ...     print(session.query(enwiki.revision_userindex)
            ...           .filter_by(rev_user_text="EpochFail")
            ...           .count())
            ...
            4302
            >>> result = enwiki.execute("SELECT COUNT(*) FROM revision_userindex " +
            ...                         "WHERE rev_user=:user_id",
            ...                         {'user_id': 6396742})
        
            >>>
            >>> print(result.fetchone())
            (4302,)
        
        ## Authors
        * Aaron Halfaker -- https://github.com/halfak
        
Platform: UNKNOWN
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3 :: Only
Classifier: Environment :: Other Environment
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Operating System :: OS Independent
Classifier: Topic :: Software Development :: Libraries :: Python Modules
Classifier: Topic :: Utilities
Classifier: Topic :: Scientific/Engineering
