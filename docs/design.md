# Design outline

As outlined on the landing page, the goal of the Turtle Canon tool is to canonize (or standardize) the Turtle ontology files exported by, especially, [Protégé](https://protege.stanford.edu/).

To achieve this, [RDFlib](https://rdflib.readthedocs.io/) is utilized to load in the Turtle file as a `rdflib.Graph` object, retrieving all the triples, sorting them, creating an empty, new `rdflib.Graph` object, add the sorted list of triples, and then export the ontology as a Turtle file, overwriting the original Turtle file.

In this process, precautions are taken to ensure the Turtle file is *only* overwritten if everything has gone as expected and an extensive validation of the input Turtle file is undertaken before even parsing it as a `rdflib.Graph` object.

## Same ontology - different generation tools

For the use case of having the same ontology, but in a logically different state, e.g., when triples may be added upon reasoning an ontology, but it is still considered to be the same ontology, the canonization process falters.
It falters in the sense that Turtle Canon considers the provided list of triples to be the ultimate source of truth for canonization.
Turtle Canon will **not** try to reason or infer what set of triples have been added during a reasoning process, and which were the "original".
It will instead merely retrieve the list of triples, sort them, and export them as a Turtle file, overwriting the source Turtle file.

### `diff` tool

It is the intention to add a `diff`-like tool for these events, where the differing set of triples are listed when comparing two Turtle files.

From there, adding functionality to interactively manipulate which triples should be created or removed should be somewhat straight-forward.
The intention is to add exactly this, however, the exact design for this has not yet been determined.

The initial point of this tool is to help users be aware that changes have occurred between two ontologies, what they are, and understand whether they are semantic or logical.
