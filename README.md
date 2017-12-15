# Morphology Pre-annotation Tool

*My Tool does one thing, and one thing well.*

In order to ease manually tagging our texts for the gold corpus, 
a pre-annotation tool which takes into account existing annotated 
texts has been designed. This tool fills in unambiguous fields for 
each word and propose alternatives in columns following the CDLI-CoNLL 
columns for the user to copy and paste the best choice.


# Installation

If you don't use `pip`, you're missing out.
Here are [installation instructions](https://pip.pypa.io/en/stable/installing/).

Simply run:

```bash
    $ git clone https://github.com/cdli-gh/morphology-pre-annotation-tool.git
    $ cd morphology-pre-annotation-tool
    $ pip install .
```
    
Or you can just do 

    $ pip install git+git://github.com/cdli-gh/morphology-pre-annotation-tool.git
    
Or you can also do  

    $ pip install git+https://github.com/cdli-gh/morphology-pre-annotation-tool.git   
    
# Upgrading
    
If you already have installed it and want to upgrade the tool:

```bash
    $ cd morphology-pre-annotation-tool
    $ git pull origin master
    $ pip install . --upgrade
```    

Or you can just do 

    $ pip install git+git://github.com/cdli-gh/morphology-pre-annotation-tool.git --upgrade
    
Or you can also do  

    $ pip install git+https://github.com/cdli-gh/morphology-pre-annotation-tool.git --upgrade
    

# Usage

To use it:

    $ cdli-mpa-tool --help
    
To run it on file:
    
    $ cdli-mpa-tool -i ./resources/P115087.conll 
    
To run it on folder:

    $ cdli-mpa-tool -i ./resources    
    

To feed the dictionary with an annotated file, use the --no_output switch :

    $ cdli-mpa-tool --no-output ./resources    
    
    

If you don't give arguments, it will prompt for the path.

The annotated dictionary is stored as [json] in the home folder of the user which runs Python (will be root if you installed Python at the system level)

(./cdli_mpa_tool/annotated_morph_dict.json) and it gets updated every time, 
so you can copy it from the path and share it.

Its structure is (FORM: [[SEGM1	XPOSTAG1], [SEGM2	XPOSTAG2]]):

```json
{
  "pisan-dub-ba": [["bisajdubak", "N"]], 
  "hu-hu-nu-ri{ki}": []
}
```
    

