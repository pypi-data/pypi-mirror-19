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

Description: # MediaWiki reverts
        
        This library provides a set of utilities for detecting reverting activity in
        MediaWiki projects.
        
        * **Installation:** ``pip install mwreverts``
        * **Documentation:** https://pythonhosted.org/mwreverts
        * **Repositiory:** https://github.com/mediawiki-utilities/python-mwreverts
        * **License:** MIT
        
        ## Basic example
        
            >>> import mwreverts
            >>>
            >>> checksum_revisions = [
            ...     ("aaa", {'rev_id': 1}),
            ...     ("bbb", {'rev_id': 2}),
            ...     ("aaa", {'rev_id': 3}),
            ...     ("ccc", {'rev_id': 4})
            ... ]
            >>>
            >>> list(mwreverts.detect(checksum_revisions))
            [Revert(reverting={'rev_id': 3},
                    reverteds=[{'rev_id': 2}],
                    reverted_to={'rev_id': 1})]
        
        ## Author
        * Aaron Halfaker -- https://github.com/halfak
        
        ## See also 
        * https://meta.wikimedia.org/wiki/Research:Revert
        
Platform: UNKNOWN
