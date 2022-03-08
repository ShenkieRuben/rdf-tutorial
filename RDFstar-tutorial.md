## Complex modelling

Below some examples of how to model complex relationships in RDF

#### 1. Standard reification

Example: 

```
:bob :hasSpouse :alice .
:id1 rdf:type rdf:Statement ;
    rdf:subject :bob ;
    rdf:predicate :hasSpouse ;
    rdf:object :alice ;
    :startDate "2020-02-11"^^xsd:date .
```

Exercise 1: 

1. Try to draw the example above in a draw.io drawing, in which individuals are represented by circles, and literals in quotes. 

2. Come up with a reified RDF representation of the statement "the Kyev Independent reported on March the 7th that person A and person B were killed in an attack". 



#### 2. N-ary relations

Example: 
```
:marriage1 rdf:type :marriage ;
    :partner1 :bob ;
    :partner2 :alice ;
    :startDate "2020-02-11"^^xsd:date .
```

Exercise 2: 

1. Try to draw the example above in a draw.io drawing, in which individuals are represented by circles, and literals in quotes. 

2. Come up with an rdf-star representation of the statement "Einstein worked at Princeton University between 1933 and 1955".

3. Can you also represent the statements from exercise 1.2 in an n-ary representation? 


#### 3. Named Graphs (TriG notation)

Example: 

```
@prefix : <http://www.example.org/> .
:statementId#1 { :bob :hasSpouse :alice }
:statementId#1 :startDate "2020-02-11"^^xsd:date .
```

Exercise 3: 

1. Try to draw the example above in a draw.io drawing, in which individuals are represented by circles, and literals in quotes. 

2. Can you also represent the statements from exercise 1.2 and 2.2 in an n-ary representation? 


#### 4. RDF-star

Example:


```
:bob :hasSpouse :alice .
<<:bob :hasSpouse :alice>> :startDate "2020-02-11"^^xsd:date .

```

Exercise 4: 

1. Try to draw the example above in a draw.io drawing, in which individuals are represented by circles, and literals in quotes. 

2. Can you also represent the statements from exercise 1.2 and 2.2 in rdf-star? 


# Creating RDF-star triples

Taking the RDF-star example above

```
:bob :hasSpouse :alice .
<<:bob :hasSpouse :alice>> :startDate "2020-02-11"^^xsd:date .
```

Note that :hasSpouse is a symmetric relation so that it can be inferred in the opposite direction. However, the metadata in the opposite direction is not asserted automatically, so it needs to be added. The file will look like:

```
:bob :hasSpouse :alice .
<<:bob :hasSpouse :alice>> :startDate "2020-02-11"^^xsd:date .
<<:alice :hasSpouse :bob>> :startDate "2020-02-11"^^xsd:date .
```

#### Expressing data certainty

```
<<:bob :hasSpouse :alice>> :startDate "2020-02-11"^^xsd:date .
<<:bob :hasSpouse :alice>> :certainty 0.4 .
```

#### A nesting example

```
<< <<:bob :hasSpouse :alice>> :startDate "2020-02-11"^^xsd:date >>
    :webpage <http://nationalenquirer.com/news/2020-02-12> .
```


#### Expressing data value qualifiers

```
<<:painting :height 32.1>>
  :unit :cm;
  :measurementTechnique :laserScanning;
  :measuredOn "2020-02-11"^^xsd:date.
```

But consider another modelling with intermediary nodes.

```
<< :painting1 :heightInCm 32.1 >>
  :measured [
    :measurementTechnique :laserScanning;
    :measuredOn "2020-02-11"^^xsd:date;
  ],[
    :measurementTechnique :measuringTape;
    :measuredOn "2020-02-12"^^xsd:date;
  ].
```

#### Expressing data provenance

```
<<:bob :hasSpouse :alice>>
  :source :TheNationalEnquirer;
  :webpage <http://nationalenquirer.com/news/2020-02-12>;
  :retrieved "2020-02-13"^^xsd:dateTime.
```

But consider another modelling with intermediary nodes.


```
<<:man :hasSpouse :woman>>
  :reference [
    :source :theNationalEnquirer;
    :webpage <http://nationalenquirer.com/news/2020-02-12>;
    :retrieved "2020-02-13"^^xsd:dateTime
  ],[
    :source :theNewYotkTime;
    :webpage <http://nytimes.com/news/2020-02-13>;
    :retrieved "2020-02-13"^^xsd:dateTime
  ].
  
```


# Basic SPARQL-star queries

List all metadata for the given reference to a statement

```
PREFIX : <http://example.org/>

SELECT *
WHERE {
    <<?man :hasSpouse :alice>> ?p ?o
    FILTER (?man = :bob)
}
```

Binding nested triples. Note that SPARQL-star modifies the BIND clauses to select a group of embedded triples by using free variables. In the following example, the generated triple is is not known in advance, and it could not have been produced directly.

```
PREFIX : <http://example.org/>

SELECT ?t 
WHERE {
    <<?man :hasSpouse :woman >> ?p ?o
    BIND(<<:woman :hasSpouse ?man>> as ?t)   
}

```

Exercise 5: 

1. upload the rdf-star snippets you created in 4.2 into GraphDB (note that you can copy snippets directly for import into your graph). Include additional statements inspired by the examples above (data certainty, provenance, nesting, etc.) to experiment with the syntax. 

2. write the following queries in SPARQL-star: 
    - who reported that two people were killed on march 7th? 
    - when did Einstein work in Princeton? 
    

# Converting RDF to RDF-star using GraphDB CONSTRUCT



```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
CONSTRUCT {
    <<?subject ?predicate ?object>> ?p ?o .
} WHERE {
    ?reification a rdf:Statement .
    ?reification rdf:subject ?subject .
    ?reification rdf:predicate ?predicate .
    ?reification rdf:object ?object .
    ?reification ?p ?o .
    FILTER (?p NOT IN (rdf:subject, rdf:predicate, rdf:object) &&
    (?p != rdf:type && ?object != rdf:Statement))
}
```

Exercise: 

Upload your reified statements (exercise 1), or any other reified statements, and transform them to the rdf-star syntax using a construct query. 