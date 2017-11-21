# Morphology Pre-annotation Tool

My Tool does one thing, and one thing well.


# Installation

If you don't use `pipsi`, you're missing out.
Here are [installation instructions](https://github.com/mitsuhiko/pipsi#readme).

Simply run:

    $ pipsi install .


# Usage

To use it:

    $ cdli-mpa-tool --help
    
To run it on file:
    
    $ cdli-mpa-tool -i ./resources/P115087.conll 
    
To run it on folder:

    $ cdli-mpa-tool -i ./resources    
    
If you don't give arguments, it will prompt for the path.

The annotated dictionary is stored as json and it gets updated every time, 
so you can copy it from the path and share it.

Its structure is (FORM: [[SEGM1	XPOSTAG1], [SEGM2	XPOSTAG2]]):

```json
{
  "pisan-dub-ba": [["bisajdubak", "N"]], 
  "hu-hu-nu-ri{ki}": []
}
```
    

