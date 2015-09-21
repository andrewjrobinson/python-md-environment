##
# BSD 3-clause licence
#
# Copyright (c) 2015, Andrew Robinson
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the names of python-md-environment AND/OR mdx_environment nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##

'''
A python markdown extension which creates sections of output that can be changed based on Environment Variables

Adds tags (latex style)

\env{ENVVAR}
\env{ENVVAR}{OPERATOR}

where OPERATOR is:
- lower: e.g. hello world
- upper: e.g. HELLO WORLD
- title: e.g. Hello World
- sentence: e.g. Hello world
- default: i.e. left unchanged, which is default operation

....

\ifdef{ENVVAR OPER VALUE}

\endifdef

where OPER:
- 

....

\if{ENVVAR}{VALUE}

\elif{ENVVAR}{VALUE2}

\else

\endif

Created on 21/09/2015
@author: Andrew Robinson
'''

from __future__ import absolute_import
from __future__ import unicode_literals

import sys
import markdown
from markdown.blockprocessors import BlockProcessor, ListIndentProcessor
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree
import os
import re

## Set the version Number
__version__ = '0.1.0'


ENVPATTERN = r'\\env{(?P<env>[^}]*)}({(?P<oper>[^}]*)})?'

class EnvironmentPattern(Pattern):
    _id = 0
    
    def handleMatch(self, m):
        
        matchVars = m.groupdict()
        
        # get my id
        myid = self._id
        self._id += 1
        
        # compute values
        val = os.environ.get(matchVars['env'])
        oper = matchVars.get('oper', '')
        if oper is None:
            oper = ""
        oper = oper.lower()
        if oper == 'upper':
            val = val.upper()
        elif oper == 'lower':
            val = val.lower()
        elif oper == 'title':
            val = val.title()
        elif oper == 'sentence':
            val = val.lower()
            if len(val) > 0:
                val = val[0].upper() + val[1:]
        #end if
        
        # make the output
        spanenv = etree.Element('span')
        spanenv.set("id", "env%s" % (myid, ))
        spanenv.set("class", "environment_env")
        spanenv.text = val
        
        return spanenv


# class EnvironmentProcessor(BlockProcessor):
#     """Create sections of output that can be changed based on Environment Variables"""
#     
#     REenv = re.compile(r'^(?P<pre>.*)\\env{(?P<env>[^}]*)}({(?P<oper>[^}]*)})?(?P<post>.*)$',re.DOTALL)
#     
#     
# #     REstart = re.compile(r'^(?P<pre>.*)\\showable(?P<mod>[+]?){(?P<title>[^}|]*)(\|(?P<hidetitle>[^}|]+))?}({(?P<class>[a-zA-Z0-9_ ]*)})?(?P<post>.*)$',re.DOTALL)
# #     REend = re.compile(r'^(?P<pre>.*)\\endshowable(?P<post>.*)$',re.DOTALL)
#     _id = 0
#     _first = True
#     
#     def test(self, parent, block):
#         return bool(self.REenv.search(block))
#     
#     def run(self, parent, blocks):
#         raw_block = blocks.pop(0)
#         matchEnv = self.REenv.search(raw_block)
#         if matchEnv is not None:
#             matchVars = matchEnv.groupdict()
#             
#             if matchVars['pre'] != '':
#                 blocks.insert(0,matchVars['pre'])
#                 blocks.insert(1,raw_block[len(matchVars['pre']):])
#             else:
#                 
#                 # get my id
#                 myid = self._id
#                 self._id += 1
#                 
#                 # compute values
#                 val = os.environ.get(matchVars['env'])
#                 oper = matchVars.get('oper', '')
#                 if oper is None:
#                     oper = ""
#                 oper = oper.lower()
#                 if oper == 'upper':
#                     val = val.upper()
#                 elif oper == 'lower':
#                     val = val.lower()
#                 elif oper == 'title':
#                     val = val.title()
#                 elif oper == 'sentence':
#                     val = val.lower()
#                     if len(val) > 0:
#                         val = val[0].upper() + val[1:]
#                 #end if
#                 
#                 # make the output
#                 spanenv = etree.SubElement(parent, 'span')
#                 spanenv.set("id", "env%s" % (myid, ))
#                 spanenv.set("class", "environment_env")
#                 spanenv.text = val
#             # endif
#         # endif
#     # end run()
#             
#     def _removeUntilMatching(self, blocks):
#         
#         myblocks = []
#         depth = 1
#         while len(blocks) > 0:
#             raw_block = blocks.pop(0)
#             matchStart = self.REstart.search(raw_block)
#             matchEnd = self.REend.search(raw_block)
#             if matchStart is not None:
#                 depth += 1
#             elif matchEnd is not None:
#                 if matchEnd.groupdict()['pre'].strip() != "":
#                     myblocks.append(matchEnd.groupdict()['pre'].strip())
#                 if matchEnd.groupdict()['post'].strip() != "":
#                     blocks.insert(0, matchEnd.groupdict()['post'].strip())
#                 depth -= 1
#                 if depth <= 0:
#                     break
#             # endif
#             
#             myblocks.append(raw_block)
#         # next block
#         
#         return myblocks

class EnvironmentExtension(Extension):
    """ Add definition lists to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of EnvironmentExtension to BlockParser. """
#         md.parser.blockprocessors.add('environment',
#                                       EnvironmentProcessor(md.parser),
#                                       '>ulist')
        md.inlinePatterns.add('environmentpattern', EnvironmentPattern(ENVPATTERN), '_begin')
        
        

def makeExtension(*args, **kwargs):
    return EnvironmentExtension(*args, **kwargs)

# ----- TESTING -----
mdtext = '''
This is a paragraph and this should be --special--

Today we will be using \env{UNIXHOSTNAME}{upper}

This is a line with the hostname: \env{UNIXHOSTFULL} and port: \env{UNIXPORT}

**Bold**: \env{UNIXHOSTSHORT}

\env{HOSTNAME}\env{UNIXHOSTSHORT}
scp -P \env{UNIXPORT} \env{UNIXHOSTFULL}:result.txt .

helloworld
'''

if __name__ == "__main__":
    
    os.environ['UNIXHOSTFULL'] = "lims-hpc-m.latrobe.edu.au"
    os.environ['UNIXHOSTSHORT'] = "lims-hpc-m"
    os.environ['UNIXHOSTNAME'] = "lims-hpc"
    os.environ['UNIXPORT'] = "6022"
    
    print (mdtext)
    print ("------")
    print (markdown.markdown(mdtext, [EnvironmentExtension(None)]))
