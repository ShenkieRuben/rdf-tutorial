from unicodedata import name
import pandas as pd
from rdflib import Graph, Literal, Namespace, RDF, URIRef, OWL
from rdflib.namespace import DC, FOAF

from owlready2 import *


onto = get_ontology("http://www.art.com/onto/")

with onto:
    # Classes
    class Painter(Thing):
        pass

    class Movement(Thing):
        pass

    class Painting(Thing):
        pass

    class Museum(Thing):
        pass

    class Location(Thing):
        pass

    # Properties
    # Painter --> ...
    class paints(Painter >> Painting):
        pass

    class bornIn(DataProperty, FunctionalProperty):
        domain = [Painter]
        range = [Location]

    class birthDate(Painter >> str):
        pass

    # Painting --> ...
    class isPaintedBy(Painting >> Painter):
        inverse_property = paints

    class inStyle(Painting >> Movement):
        pass

    class locatedIn(Painting >> Museum):
        pass

    class located(Museum >> Location):
        pass


# 4 Links to linked open data
# https://dbpedia.org/page/Pablo_Picasso --> Pablo Picasso
# https://dbpedia.org/page/Impressionism --> Impressionism
# https://dbpedia.org/page/The_Starry_Night --> Starry Night
# https://dbpedia.org/page/Louvre --> Louvre Museum

# Note that in my ontology, for simplicity's sake, all the data from the tables are literals. I am aware of the fact that we can turn these literals into subclasses and then use owl:sameAs statements to link them with resources from LOD.

# Now for the instances

# Locations
zundert = Location(name="Zundert")
florence = Location(name="Florence")
limoges = Location(name="Limoges")
malaga = Location(name="Malaga")

new_york = Location(name="New York")
paris = Location(name="Paris")
washington = Location(name="Washington")
madrid = Location(name="Madrid")

# Movements
impressionism = Movement(name="Impressionism")
renaissance = Movement(name="Renaissance")
cubism = Movement(name="Cubism")

# Museums
moma = Museum(name="MOMA", located=new_york)
louvre = Museum(name="Louvre", located=paris)
pc = Museum(name="Phillips Collection", located=washington)
rs = Museum(name="Reina Sofia", located=madrid)


starry_night = Painting(Name="Starry Night", inStyle=impressionism, locatedIn=moma)
la_gioconda = Painting(Name="La Gioconda", inStyle=renaissance, locatedIn=louvre)
luncheon = Painting(
    name="Luncheon of the Boating Party", inStyle=impressionism, locatedIn=pc
)
guernica = Painting(name="Guernica", inStyle=cubism, locatedIn=rs)


van_gogh = Painter(
    name="Van Gogh", birthDate="1853-03-30", bornIn=zundert, paints=starry_night
)
da_vinci = Painter(
    name="Da Vinci", birthDate="1452-04-15", bornIn=florence, paints=la_gioconda
)
renoir = Painter(name="Renoir", birthDate="1841-02-25", bornIn=limoges, paints=luncheon)
picasso = Painter(
    name="Picasso", birthDate="1881-10-25", bornIn=malaga, paints=guernica
)
