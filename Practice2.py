from mailbox import MaildirMessage
from opcode import haslocal
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

    class Country(Thing):
        pass

    class City(Thing):
        pass

    class US(Country):
        pass

    class Spain(Country):
        pass

    class France(Country):
        pass

    class Italy(Country):
        pass

    class Holland(Country):
        pass

    # Properties
    # Painter --> ...
    class paints(Painter >> Painting):
        pass

    class bornIn(ObjectProperty, FunctionalProperty):
        domain = [Painter]
        range = [City]

    class birthDate(Painter >> str, FunctionalProperty):
        pass

    # Painting --> ...
    class isPaintedBy(Painting >> Painter):
        inverse_property = paints

    class inStyle(Painting >> Movement):
        pass

    class isIn(Thing >> Thing, TransitiveProperty):
        pass

    # 4 Links to linked open data
    # https://dbpedia.org/page/Pablo_Picasso --> Pablo Picasso
    # https://dbpedia.org/page/Impressionism --> Impressionism
    # https://dbpedia.org/page/The_Starry_Night --> Starry Night
    # https://dbpedia.org/page/Louvre --> Louvre Museum

    # Note that in my ontology, for simplicity's sake, all the data from the tables are literals. I am aware of the fact that we can turn these literals into subclasses and then use owl:sameAs statements to link them with resources from LOD.

    # Now for the instances

    # Movements
    impressionism = Movement(name="Impressionism")
    renaissance = Movement(name="Renaissance")
    cubism = Movement(name="Cubism")

    # Countries
    us = US("Verenigde_Staten")
    spain = Spain("Spanje")
    france = France("Frankrijk")
    holland = Holland("Nederland")
    italy = Italy("Italië")

    # Cities
    washington = City("Washington", isIn=[us])
    madrid = City("Madrid", isIn=[spain])
    paris = City("Paris", isIn=[france])
    new_york = City("New_York", isIn=[us])

    # Birth places
    zundert = City("Zundert", isIn=[holland])
    florence = City("Florence", isIn=[italy])
    limoges = City("Limoges", isIn=[france])
    malaga = City("Malaga", isIn=[spain])

    # # Museums
    moma = Museum(name="MOMA", isIn=[new_york])
    louvre = Museum(name="Louvre", isIn=[paris])
    pc = Museum(name="Phillips_Collection", isIn=[washington])
    rs = Museum(name="Reina_Sofia", isIn=[madrid])

    starry_night = Painting(name="Starry_Night", inStyle=[impressionism], isIn=[moma])
    la_gioconda = Painting(name="La_Gioconda", inStyle=[renaissance], isIn=[louvre])
    luncheon = Painting(
        name="Luncheon_of_the_Boating_Party", inStyle=[impressionism], isIn=[pc]
    )
    guernica = Painting(name="Guernica", inStyle=[cubism], isIn=[rs])

    van_gogh = Painter(
        name="Van_Gogh",
        birthDate="1853-03-30",
        bornIn=zundert,
        paints=[starry_night],
    )
    da_vinci = Painter(
        name="Da_Vinci", birthDate="1452-04-15", bornIn=florence, paints=[la_gioconda]
    )
    renoir = Painter(
        name="Renoir", birthDate="1841-02-25", bornIn=limoges, paints=[luncheon]
    )
    picasso = Painter(
        name="Picasso", birthDate="1881-10-25", bornIn=malaga, paints=[guernica]
    )

    onto.save("./data/practical2.owl")
