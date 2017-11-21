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

    $ pip install .


# Usage

To use it:

    $ cdli-mpa-tool --help
    
To run it on file:
    
    $ cdli-mpa-tool -i ./resources/P115087.conll 
    
To run it on folder:

    $ cdli-mpa-tool -i ./resources    
    
If you don't give arguments, it will prompt for the path.

The annotated dictionary is stored as [json](./cdli_mpa_tool/annotated_morph_dict.json) and it gets updated every time, 
so you can copy it from the path and share it.

Its structure is (FORM: [[SEGM1	XPOSTAG1], [SEGM2	XPOSTAG2]]):

```json
{
  "pisan-dub-ba": [["bisajdubak", "N"]], 
  "hu-hu-nu-ri{ki}": []
}
```
    

