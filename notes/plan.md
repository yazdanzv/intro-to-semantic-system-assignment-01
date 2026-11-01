# Assignment 01: Travel Assistant — Decisions and Working Notes

This is the central working record for our decisions, definitions, questions, and checks at each assignment step. Update it as the model develops; use it to inform the separate final report in `../report/report.md`.

**Last updated:** 2 November 2026.

**Status meanings:** Agreed = accepted direction; Proposed = an option still to review; Pending = not yet decided; Not performed = no execution or validation evidence yet.

## Progress

| Step | Work | Status |
|---|---|---|
| 1 | Application idea and scope | Agreed; recorded below |
| 2 | Competency questions | Eight questions agreed; recorded below |
| 3 | Classes and hierarchy | 18 domain classes and their hierarchy agreed; recorded below |
| 4 | Object and datatype properties | 26 properties agreed: 13 object and 13 datatype properties, including the Step 6 inverse |
| 5 | RDF(S) model, identifiers, labels, and comments | Agreed and implemented; Turtle parsing and structural checks passed |
| 6 | OWL extensions | Five construct kinds agreed and implemented |
| 7 | Validation and question coverage | Parser, structural, Protégé loading, consistency, and named-class satisfiability checks passed for version 0.2; all eight competency questions covered at schema level |
| 8 | Final report | Three-page PDF and editable DOCX written and visually checked; ready for student review |
| 9 | Export and TUWEL submission | Report PDF prepared; final ontology export and TUWEL upload pending |

## Step 1 — Application idea and scope

**Status: Agreed.** The chosen direction is a travel assistant for planning city trips. The agreed class vocabulary and hierarchy are recorded in Step 3 and properties in Step 4. The RDF(S) baseline is preserved in Step 5; five richer OWL construct kinds are agreed and implemented in Step 6.

### Decision table

| Decision | Agreed direction | Concepts agreed in Step 3 |
|---|---|---|
| Domain | Tourism and city-trip planning | `Place`, `City`, `Country` |
| Users | People planning a leisure trip | `Traveler` |
| Purpose | Help travelers decide where to go, what to do, and where to stay | Connections between destinations, places, activities, and preferences |
| Destination information | Represent cities and their countries | `City`, `Country` |
| Places to visit | Describe attractions and their categories | `Attraction`, `Museum`, `Landmark`, `Park` |
| Things to do | Describe activities and the interests they suit | `Activity`, `Interest` |
| Accommodation | Represent places to stay and their categories | `Accommodation`, `Hotel`, `Hostel` |
| Food | Represent restaurants and the cuisines they serve | `Restaurant`, `Cuisine` |
| Transport | Describe ways to reach destinations or attractions | `TransportOption`, `TransportMode` |
| Personal preferences | Match options to interests and broad budget categories | `Interest`, `BudgetCategory` |
| Outside scope | Bookings, payments, visa advice, live availability, and real-time prices | Not modeled in the initial scope |

### Application description

We propose a travel assistant that helps leisure travelers plan city trips. It would connect destinations with attractions, activities, accommodation, restaurants, and transport options, allowing travelers to explore choices based on their interests and budget category. Booking transactions and information requiring live updates are outside the initial scope.

### Semantic benefit

Explicit relationships would let the imagined application connect a traveler's interests to suitable activities and attractions, locate those options within destinations, and identify related accommodation and transport options. These are intended capabilities, not implemented or tested features.

### Open details to resolve later

- Define what a `TransportOption` represents and how it differs from a `TransportMode`.
- Decide how budget categories are assigned; do not imply current prices or availability.
- Define how traveler preferences connect to interests and budget categories. A separate `TripPlan` class is omitted from the agreed initial model (see Step 3).
- Choose geographic coverage if needed; no particular cities or countries have been selected.

## Step 2 — Competency questions

**Status: Agreed.** The following eight competency questions define the intended coverage of the travel assistant and satisfy the requirement for 5–10 questions. They guide the next class and property modeling steps.

| ID | Agreed question | Information the model would need | Status |
|---|---|---|---|
| CQ-01 | Which attractions are located in a selected city? | Attractions, cities, locations | Agreed |
| CQ-02 | Which attractions in that city match the traveler’s interests? | Attractions, interests, traveler preferences | Agreed |
| CQ-03 | Which activities are available in that city and match those interests? | Activities, cities, interests | Agreed |
| CQ-04 | Which accommodation options in that city match the traveler’s budget category? | Accommodation, cities, budget categories | Agreed |
| CQ-05 | Which hotels or hostels are located in the selected city? | Accommodation types and locations | Agreed |
| CQ-06 | Which restaurants in that city serve a preferred cuisine? | Restaurants, cities, cuisines | Agreed |
| CQ-07 | Which transport options provide access to a selected attraction? | Transport options, modes, attractions | Agreed |
| CQ-08 | Which cities offer attractions matching the traveler’s interests? | Cities, attractions, interests | Agreed |

Here, “that city” refers to the city selected by the traveler. “Available” describes activities associated with a city, rather than live booking availability. The interpretations used for matching and access are recorded in the Step 7 coverage review; criteria for assigning real data remain outside this assignment.

For each question, record the final classes and properties needed as the ontology develops. The questions are agreed requirements, not evidence of implemented functionality. Actual query answers and SPARQL queries have not been produced.

## Step 3 — Classes and hierarchy

**Status: Agreed.** The following 18 domain classes and their parent relationships are accepted for the initial model. This exceeds the requirement for at least 15 concepts/classes without counting the built-in `owl:Thing`. They are implemented in the baseline ontology described in Step 5.

### Agreed classes

| Class | Parent class | Meaning |
|---|---|---|
| `Place` | `owl:Thing` | A geographic area or physical location |
| `City` | `Place` | A city the traveler could visit |
| `Country` | `Place` | A country containing travel destinations |
| `Attraction` | `Place` | A place travelers may visit for interest or enjoyment |
| `Museum` | `Attraction` | An attraction displaying collections or exhibitions |
| `Landmark` | `Attraction` | A notable site or structure |
| `Park` | `Attraction` | A public outdoor area for recreation |
| `Accommodation` | `Place` | A place providing overnight stays |
| `Hotel` | `Accommodation` | Hotel accommodation |
| `Hostel` | `Accommodation` | Hostel accommodation |
| `Restaurant` | `Place` | A place serving meals |
| `Traveler` | `owl:Thing` | A person whose travel preferences we represent |
| `Interest` | `owl:Thing` | A topic the traveler enjoys, such as history |
| `Activity` | `owl:Thing` | Something travelers can do, such as a guided tour |
| `Cuisine` | `owl:Thing` | A culinary tradition or style |
| `BudgetCategory` | `owl:Thing` | A broad cost category, with criteria to define later |
| `TransportOption` | `owl:Thing` | A transport service or connection providing access to a place |
| `TransportMode` | `owl:Thing` | A type of transport, such as bus or rail |

### Agreed hierarchy

```text
owl:Thing
├── Place
│   ├── City
│   ├── Country
│   ├── Attraction
│   │   ├── Museum
│   │   ├── Landmark
│   │   └── Park
│   ├── Accommodation
│   │   ├── Hotel
│   │   └── Hostel
│   └── Restaurant
├── Traveler
├── Interest
├── Activity
├── Cuisine
├── BudgetCategory
├── TransportOption
└── TransportMode
```

### Hierarchy decisions and rationale

- Use `Place` as the shared superclass for geographic areas and physical locations.
- Use `City` to represent the selected city destination; omit a separate `Destination` class from the initial model.
- Omit `TripPlan` initially because the eight agreed competency questions can be supported without it.
- Keep classes such as `Traveler`, `Activity`, and `Interest` as top-level domain classes under `owl:Thing`. A more specific superclass is only needed when it expresses a useful shared meaning.
- Interpret every subclass relationship as “is a kind of”: every member of the subclass must also belong to its parent. For example, every museum is an attraction and therefore also a place.
- Represent location and part-of connections with properties in Step 4. A city is located in a country; it is not a subclass of `Country`.
- Connect individuals across class branches using properties in Step 4. Being a top-level class does not mean being disconnected from the rest of the ontology.
- Different branches are not automatically disjoint. Step 6 explicitly declares `Traveler` disjoint with `Place`; other branches are not declared disjoint.

**Individuals and real-world data:** None selected or collected. The terms above name categories, not individual destinations, hotels, or travelers. Instances are not required for Assignment 1.

## Step 4 — Object and datatype properties

**Status: Agreed.** The current set contains 26 domain properties: 13 object properties and 13 datatype properties. The original Step 4 set contained 25 properties; Step 6 adds the agreed inverse property `containsPlace`. This exceeds the requirement for at least 20 properties and includes both required types. Labels and comments are separate annotations and are not counted here. The properties are implemented; parser/structural checks and the Protégé/HermiT checks documented in Step 7 have passed.

### Agreed object properties

| Property | Domain | Range | Meaning | Question coverage |
|---|---|---|---|---|
| `locatedInCity` | `Place` | `City` | A place is located in a city | CQ-01, CQ-02, CQ-04, CQ-05, CQ-06, CQ-08 |
| `containsPlace` | `City` | `Place` | A city contains a place; added in Step 6 as the inverse of `locatedInCity` | Reverse lookup for CQ-01, CQ-02, CQ-04, CQ-05, CQ-06, CQ-08 |
| `locatedInCountry` | `City` | `Country` | A city is located in a country | Geographic context |
| `hasInterest` | `Traveler` | `Interest` | A traveler has an interest | CQ-02, CQ-03, CQ-08 |
| `hasAttractionTheme` | `Attraction` | `Interest` | An attraction relates to an interest | CQ-02, CQ-08 |
| `hasActivityTheme` | `Activity` | `Interest` | An activity relates to an interest | CQ-03 |
| `activityInCity` | `Activity` | `City` | An activity takes place in a city | CQ-03 |
| `hasBudgetCategory` | `Accommodation` | `BudgetCategory` | Accommodation belongs to a cost category | CQ-04 |
| `prefersBudgetCategory` | `Traveler` | `BudgetCategory` | A traveler prefers a cost category | CQ-04 |
| `servesCuisine` | `Restaurant` | `Cuisine` | A restaurant serves a cuisine | CQ-06 |
| `prefersCuisine` | `Traveler` | `Cuisine` | A traveler prefers a cuisine | CQ-06 |
| `providesAccessTo` | `TransportOption` | `Attraction` | A transport option provides access to an attraction | CQ-07 |
| `usesTransportMode` | `TransportOption` | `TransportMode` | A transport option uses a mode, such as rail | Transport context for CQ-07 |

### Agreed datatype properties

The `xsd:` prefix refers to the standard XML Schema datatype namespace, `http://www.w3.org/2001/XMLSchema#`.

| Property | Domain | Datatype | Meaning |
|---|---|---|---|
| `hasPlaceName` | `Place` | `xsd:string` | The place's name |
| `hasStreetAddress` | `Place` | `xsd:string` | A street address, where applicable |
| `hasWebsite` | `Place` | `xsd:anyURI` | The place's website address |
| `hasCountryCode` | `Country` | `xsd:string` | A country code |
| `hasActivityName` | `Activity` | `xsd:string` | The activity's name |
| `hasDurationMinutes` | `Activity` | `xsd:nonNegativeInteger` | The activity's duration in minutes |
| `hasTransportName` | `TransportOption` | `xsd:string` | The transport service or connection's name |
| `hasRouteIdentifier` | `TransportOption` | `xsd:string` | A route identifier, where applicable |
| `hasCurrencyCode` | `Country` | `xsd:string` | A currency code used in the country |
| `hasTimeZone` | `City` | `xsd:string` | A time-zone identifier, such as `Europe/Vienna` |
| `hasVegetarianOptions` | `Restaurant` | `xsd:boolean` | Whether vegetarian dishes are offered |
| `hasCheckInTime` | `Accommodation` | `xsd:time` | The accommodation's standard local check-in time |
| `hasCheckOutTime` | `Accommodation` | `xsd:time` | The accommodation's standard local check-out time |

The last five rows are the selected additions to the original eight datatype properties. Latitude, longitude, and typical attraction visit duration are omitted from this agreed set. Datatype properties provide descriptive information; not all are needed directly to answer the eight competency questions.

### Interpretation and implementation notes

- Property declarations alone do not require every individual to have a value. Step 6 requires a city for every attraction and exactly one city for every accommodation. The vegetarian boolean is functional but remains optional.
- A missing boolean value means unknown rather than `false` under the open-world assumption.
- Domain and range declarations support type inference; they are not merely input-validation rules.
- A hotel or hostel is also a `Place` through the agreed hierarchy, so it can use place properties without separate duplicates for its subtype.
- Country currency codes, city time-zone identifiers, and accommodation check-in/out times describe reference information, not live prices or availability. The date/time datatypes and time-zone identifiers must be kept conceptually distinct: a local `xsd:time` is not an IANA time-zone identifier.
- Human-readable English labels and comments have been added to every property in the Step 5 baseline.

The Step 7 review uses shared interests, accommodation in an explicitly preferred budget category, and an explicitly recorded transport connection serving an attraction. Price thresholds and operational transport-access criteria for future datasets remain unspecified.

## Step 5 — RDF(S) model and documentation

**Status: Agreed and implemented.** The original basic class/property model is preserved in [the RDF(S) baseline snapshot](../ontology/baseline/travel-assistant-rdfs.owl), serialized in Turtle. The current enriched working ontology is [travel-assistant.owl](../ontology/travel-assistant.owl). The following table records the Step 5 baseline conventions; Step 6 records the later additions.

| Decision or task | Current record |
|---|---|
| Ontology IRI | `https://example.org/travel-assistant` |
| Namespace | `https://example.org/travel-assistant#` |
| Prefix | `ta:` |
| Class naming | Agreed `PascalCase` names, such as `TransportOption` |
| Property naming | Agreed `camelCase` names, such as `hasInterest` |
| Annotation language | English labels and comments tagged `en` |
| Class hierarchy | All 18 class/parent relationships from Step 3 implemented |
| Property hierarchy | No additional subproperty relationships introduced in this baseline |
| Property domains, ranges, and datatypes | All 25 declarations from Step 4 implemented |
| Labels and comments | One English label and comment on each of the 43 domain elements and on the ontology itself |
| Baseline ontology file | `ontology/baseline/travel-assistant-rdfs.owl` (preserved copy of the original version 0.1 working file) |
| Serialization | Turtle, retained with the `.owl` extension |
| Version annotation | `0.1 - RDF(S) baseline` |
| Domain individuals | None added |
| Imported domain ontologies | None |

The `example.org` identifiers are accepted coursework identifiers; no website or domain registration is required to use them. The domain vocabulary is built from scratch using the standard RDF, RDFS, OWL, and datatype vocabularies.

The preserved baseline uses OWL declarations (`owl:Ontology`, `owl:Class`, `owl:ObjectProperty`, and `owl:DatatypeProperty`) to identify entity types, while its hierarchy, domains, ranges, and annotations implement the RDF(S) foundation. These declarations do not replace the five richer OWL constructs required in Step 6. The baseline snapshot has no disjointness, inverse-property, equivalence, cardinality, or value-restriction axioms; the working ontology now includes the agreed Step 6 additions.

### Baseline checks performed

On 1 November 2026, the saved file was parsed using **Python 3.12.14 and RDFLib 7.6.0**. RDFLib was installed into an isolated temporary dependency directory; it is not a project dependency or part of the submitted ontology.

- Turtle parsing succeeded: **201 RDF triples**.
- The graph contained exactly **18 classes, 12 object properties, and 13 datatype properties**, matching the agreed names in this log.
- All 18 parent declarations and every property domain/range matched the agreed tables exactly.
- All 43 domain elements and the ontology had a nonempty label and comment tagged `en`.
- No domain individuals, imported ontologies, or deferred Step 6 axioms were present.
- Serializing the parsed graph as Turtle and parsing it again preserved the graph (graph-isomorphism check).

Checked baseline SHA-256: `7ed2c9b1fb73e46745fa055f6e556f0f74fb7a112c5666a7a20e3e96d7bb3bff`.

These were parser and structural checks of the original baseline. Subsequent Protégé loading, OWL consistency, and named-class satisfiability checks of version 0.2 are recorded in Step 7; the later schema-level question-coverage review is also recorded in Step 7.

## Step 6 — OWL extensions

**Status: Agreed and implemented on 2 November 2026.** Five different OWL construct kinds enrich the original RDF(S) baseline in `ontology/travel-assistant.owl`. The ontology version annotation is now `0.2 - Agreed OWL enrichment`.

| Construct | Formal statement (Manchester-style notation) | Meaning and purpose |
|---|---|---|
| Disjoint classes | `Traveler DisjointWith Place` | A traveler cannot also be a place. This separates people from geographic areas and venues. |
| Inverse properties | `locatedInCity InverseOf containsPlace` | If a place is located in a city, the city contains that place, and conversely. Supports lookup in both directions. |
| Existential restriction | `Attraction SubClassOf locatedInCity some City` | Every attraction is associated with at least one city in the chosen city-trip scope. |
| Qualified exact cardinality | `Accommodation SubClassOf locatedInCity exactly 1 City` | Every accommodation is associated with exactly one city as an explicit simplifying assumption. |
| Functional datatype property | `hasVegetarianOptions Characteristics: Functional` with range `xsd:boolean` | Each restaurant can have at most one yes/no value; asserting both true and false is contradictory. |

### Agreed assumptions and consequences

- Every attraction and accommodation must be associated with a city. Attractions require at least one; accommodation requires exactly one.
- The city requirements also apply to subclasses: museums, landmarks, and parks inherit the attraction requirement; hotels and hostels inherit the accommodation requirement.
- `containsPlace` is a new object property with domain `City`, range `Place`, and English label/comment. The model now has 18 named classes and 26 properties (13 object and 13 datatype properties).
- The vegetarian attribute is a single yes/no description without menu history or seasonal alternatives. It remains optional: a missing value means unknown, and does not mean false.
- These scope assumptions are modeling choices, not claims that every possible real-world attraction or accommodation obeys them.
- OWL's open-world semantics does not require the city filler to be explicitly named in the data. Missing recorded city information is not automatically a consistency error.
- OWL does not assume different identifiers name different individuals. If accommodation is linked to two city names, a reasoner may identify them as the same city; a contradiction requires evidence that the city individuals are distinct.
- The city cardinality counts distinct city individuals, not text identifiers or repeated triples. With the global `locatedInCity` range of `City`, the accommodation restriction limits all its location values to one city.
- The inverse property and restrictions add no domain individuals or travel data to the submission ontology.

### Representation in the Turtle file

The file uses `owl:disjointWith`, `owl:inverseOf`, an `owl:Restriction` with `owl:someValuesFrom`, an `owl:Restriction` with `owl:qualifiedCardinality` and `owl:onClass`, and an `owl:FunctionalProperty` declaration on `hasVegetarianOptions`. The two anonymous restrictions also have English labels and comments.

## Step 7 — Validation and question coverage

**Status: Schema-level validation complete.** Parser and structural checks were rerun on version 0.2 on 2 November 2026 using Python 3.12.14 and RDFLib 7.6.0. The Step 5 baseline snapshot was also checked for preservation. The same version was subsequently inspected in Protégé 5.6.9 and classified using HermiT 1.4.3.456. Loading, consistency, and named-class satisfiability checks passed. The schema-level review of all eight competency questions also passed, as detailed below. Individual-level behavioral tests were not performed; they are not required for this schema-only assignment. Recheck the ontology after subsequent changes.

| Check | Intended method | Result or evidence |
|---|---|---|
| Turtle syntax | Parse the saved file with RDFLib 7.6.0 | Passed: 222 triples; Turtle round-trip preserved the graph |
| Protégé loading | Open the saved ontology in Protégé 5.6.9 | Passed: the app window and log identify the correct file; ontology loading and subsequent reload completed |
| Overall consistency | Start HermiT 1.4.3.456 in Protégé | Passed: classification completed, reasoner active and synchronized, and no inconsistency reported |
| Class satisfiability | Expand and inspect the inferred class hierarchy | Passed: all 18 named domain classes appear under `owl:Thing`, with none classified as unsatisfiable |
| Expected inferences | Compare reasoner conclusions with intended meanings | Inferred class hierarchy reviewed and matches the agreed hierarchy; individual-level consequences not separately tested |
| Competency-question coverage | Map every final question to the required classes and properties | Passed at schema level: all eight questions have complete relationship patterns; declarations, domains, ranges, and inherited applicability checked with RDFLib 7.6.0 |
| Assignment counts | Count domain classes, object/datatype properties, and OWL construct kinds | Passed: 18 named classes, 26 properties, and all five agreed construct kinds present |
| Hierarchy and property definitions | Compare graph declarations with the agreed Markdown tables | Passed: named parents, domains, and ranges match, including `containsPlace` |
| OWL axiom structure | Inspect disjointness, inverse, both restrictions, functional declaration, and boolean range | Passed: exact agreed terms, city filler, cardinality 1, and datatype present |
| Annotations | Check labels and comments for all ontology elements | Passed: English labels/comments on all 44 named domain elements, the ontology, and both anonymous restrictions |
| Baseline preservation | Parse preserved snapshot and compare SHA-256 | Passed: 201 triples and the original Step 5 checksum |

Checked version 0.2 SHA-256: `0a045f6bc0a58e92b51ed092937dd02402c58350e07e0e110e7c6c2c3f46e3ba`.

### Protégé and HermiT observations

On 2 November 2026, Codex inspected the user's already-open ontology through the Protégé interface. The window title identified the expected `ontology/travel-assistant.owl` file and ontology IRI. HermiT 1.4.3.456 was selected from the Reasoner menu and started. The log recorded `Ontologies processed in 134 ms by HermiT` at `00:20:06`; the UI then showed `Reasoner active` with synchronization not required and no inconsistency warning.

The fully expanded inferred hierarchy contained all 18 named domain classes in the agreed arrangement. All were satisfiable. The interface also displayed each agreed OWL construct correctly:

- `Accommodation`: `located in city exactly 1 City`.
- `Attraction`: `located in city some City`.
- `Traveler`: disjoint with `Place`.
- `locatedInCity`: inverse of `containsPlace`, domain `Place`, range `City`.
- `hasVegetarianOptions`: Functional checked, domain `Restaurant`, range `xsd:boolean`.

The data and object property lists each displayed the 13 agreed properties, with readable labels. Representative labels and comments were inspected in the entity panels; complete annotation coverage had already been checked programmatically.

The earlier shell `java -version` failure did not prevent the app from running HermiT. Protégé's log reports **JVM 11.0.25+9**, **OWL API 4.5.29**, and **Protégé 5.6.9**. The successful app-based check supersedes the earlier runtime blocker. No ontology axioms were edited or saved during this inspection, and the working file's checksum remains the version 0.2 SHA-256 above.

These checks establish successful loading, consistency, and named-class satisfiability for the current ontology. By themselves, they do not establish real-world data accuracy, question coverage, or tested instance-level answers. The separate schema-level coverage review follows below. No synthetic or real domain individuals were added.

Record the date, tool/version, checked file version, observed result, and any fixes when checks are run. A file loading successfully or a consistency check passing does not by itself establish that the model supports every question.


### Competency-question coverage review

On 2 November 2026, all eight agreed questions were manually mapped to relationship patterns in the saved version 0.2 ontology. An additional RDFLib 7.6.0 check verified that every required class and object property exists, its domain and range fit the pattern, and subclass inheritance permits the required use. All eight checks passed. The ontology remains unchanged at 222 triples and the SHA-256 recorded above.

The following are schema patterns, not executed queries or instance data. Each shared variable denotes the same individual within its row; `traveler`, `selectedCity`, and `selectedAttraction` are inputs. Results also have the class specified in the question, including membership inherited from subclasses.

| ID | Required relationship pattern | Result |
|---|---|---|
| CQ-01 | `attraction locatedInCity selectedCity` | Covered: `Attraction` and `City` connected by `locatedInCity` |
| CQ-02 | `attraction locatedInCity selectedCity`; `traveler hasInterest interest`; `attraction hasAttractionTheme interest` | Covered: city filter and shared `Interest` |
| CQ-03 | `activity activityInCity selectedCity`; `traveler hasInterest interest`; `activity hasActivityTheme interest` | Covered: city filter and shared `Interest` |
| CQ-04 | `accommodation locatedInCity selectedCity`; `traveler prefersBudgetCategory category`; `accommodation hasBudgetCategory category` | Covered: city filter and shared `BudgetCategory` |
| CQ-05 | `hotel locatedInCity selectedCity` **or** `hostel locatedInCity selectedCity` | Covered: `Hotel` and `Hostel` inherit from `Accommodation` and `Place` |
| CQ-06 | `restaurant locatedInCity selectedCity`; `traveler prefersCuisine cuisine`; `restaurant servesCuisine cuisine` | Covered: city filter and shared `Cuisine` |
| CQ-07 | `option providesAccessTo selectedAttraction`; optionally `option usesTransportMode mode` to display its mode | Covered: `TransportOption` connects directly to `Attraction` |
| CQ-08 | `traveler hasInterest interest`; `attraction hasAttractionTheme interest`; `attraction locatedInCity city` | Covered: shared `Interest`, returning the related `City` |

**Interpretations used for this review:**

- Interest matching means sharing at least one `Interest` individual. It does not require all interests to match or calculate a similarity score. The same spelling of a label alone does not establish a shared individual.
- Budget matching means membership in the same explicitly preferred `BudgetCategory`. Categories have no price thresholds or ordering in this model: a preference for one category does not automatically include cheaper categories. Consistent assignment criteria would be needed when real data is added.
- Cuisine matching likewise uses a shared `Cuisine` individual.
- An activity being “available” means it takes place in the selected city; it does not imply date-specific or live availability.
- Transport access means an explicitly recorded service/connection-to-attraction link. `TransportMode` describes the type, such as bus or rail. Route computation, schedules, walking distances, and live service guarantees are outside scope; detailed access criteria would be needed for real data.
- Locations, themes, and preferences must be recorded or appropriately entailed to retrieve useful answers. Existential city restrictions alone do not supply a named city. Restaurants can be linked to cities, although the ontology does not require every restaurant to have a city assertion.
- The ontology supplies the vocabulary and constraints. It does not itself implement recommendation logic or generate answers. Shared-variable joins would be performed by a future query/application layer, with subclass reasoning or equivalent handling where needed.

**Conclusion:** All eight agreed questions are representable under these interpretations. No additional classes, properties, or OWL axioms are needed for their schema-level coverage. No domain individuals were added, no query answers were produced, and no instance-level behavioral tests were run. These results establish representational coverage, not the completeness or accuracy of a populated travel dataset.

## Step 8 — Report

**Status: Written and visually checked; ready for student review.** The user approved the three-page plan with two diagrams and the OWL table, provided their name and student number, and requested both Word and PDF versions. The user reports no declared AI-use/disclosure rule. The development paragraph explicitly records Codex's generation of the Turtle file from the agreed design.

The source is `../report/report.md`; the editable document is `../report/A1_ZandiyeVakili_12642780_Report.docx` and the PDF is `../submission/A1_ZandiyeVakili_12642780_Report.pdf`. Both have the same content and rendered three-page layout. Figures and their editable SVG sources are in `../report/figures/`; `../report/build_report.py` builds the document and checks diagram terms/edges against the ontology. The PDF was exported from the DOCX through the documents skill renderer. All three rendered pages were inspected after the final changes: no clipped text, broken tables, overlapping elements, or missing diagram strokes. Name, student number, all eight questions, required counts, and OWL examples were also checked.

| Required content | Working source | Status |
|---|---|---|
| Application idea in 2–3 paragraphs | Step 1 | Included as two paragraphs on page 1 |
| 5–10 competency questions | Step 2 | All eight included on page 1 |
| Development process, about one paragraph per step | Actual work recorded in Steps 1–7 | Seven paragraphs on page 2, followed by the complete class hierarchy |
| OWL features with examples | Step 6 | Five-row table on page 3, with semantic consequences explained |
| Optional reflection | Actual challenges and lessons learned | Short reflection on page 3, alongside the relationship diagram and coverage explanation |

Describe the steps actually followed and checks actually performed. Record any attribution or assistance disclosure required by the course policy.

## Step 9 — Export and submission

**Status: Report PDF prepared; final ontology export and upload pending.** Deadline: 2 November 2026. Confirm the exact cutoff in TUWEL.

| Deliverable | Required format and filename | Status |
|---|---|---|
| Ontology | Turtle syntax, saved as `A1_<family-name>_<student-number>_Ontology.owl` | Working ontology passed Protégé loading, HermiT classification, and schema-level question coverage; final export/name pending |
| Report | 2–3 page PDF, named `A1_<family-name>_<student-number>_Report.pdf` | Three-page `A1_ZandiyeVakili_12642780_Report.pdf` created and visually checked; not uploaded |

Prepare final exports in `../submission/`. In Protégé, use **File → Save As → Turtle Syntax** and retain the required `.owl` extension. Reopen the exported ontology and inspect the PDF before uploading both to TUWEL. GitHub is used for version history; it does not replace the TUWEL submission.

## Source and decision history

The authoritative brief is the local PDF in `../instructions/`. This log summarizes requirements and records working decisions; check TUWEL for updates and additional policies.

| Date | Record |
|---|---|
| 1 November 2026 | Agreed on the travel-assistant city-trip scope and its proposed scope table. Recorded the application description, candidate vocabulary, and three example competency questions. Detailed modeling and validation remain pending. |
| 1 November 2026 | Replaced the three provisional examples with the eight agreed competency questions CQ-01–CQ-08. Step 2 is agreed; detailed matching, budget, and transport-access semantics remain to be defined during modeling. |
| 1 November 2026 | Agreed on 18 domain classes and their hierarchy. Added `Place`, omitted separate `Destination` and `TripPlan` classes from the initial model, and retained meaningful top-level classes under `owl:Thing`. Property definitions, OWL extensions, and implementation remain pending. |
| 1 November 2026 | Agreed on 25 properties: the original 12 object and 8 datatype properties, plus currency code, time zone, vegetarian options, check-in time, and check-out time. The other three suggested datatype additions were omitted. Implementation and validation remain pending. |
| 1 November 2026 | Agreed on Step 5 identifiers, naming, English annotations, and Turtle serialization. Codex created the baseline ontology from the agreed decisions. RDFLib 7.6.0 parsing, table comparisons, annotation checks, and graph round-trip checks passed. Protégé loading, OWL enrichment, and reasoning remain pending. |
| 2 November 2026 | Agreed on all five Step 6 constructs, including the attraction/accommodation city requirements and the single yes/no vegetarian attribute. Preserved the original RDF(S) baseline, implemented the axioms, and added inverse property `containsPlace`. Parser, structural, annotation, and round-trip checks passed for version 0.2. HermiT was not run because the system Java command could not locate a runtime. |
| 2 November 2026 | Inspected the already-open file in Protégé 5.6.9, selected and ran HermiT 1.4.3.456, and reviewed the inferred hierarchy and all five construct kinds. Classification completed successfully; all 18 named classes are satisfiable and no inconsistency was reported. The ontology file was unchanged. Full question-coverage review remains pending. |
| 2 November 2026 | Reviewed all eight competency questions against the saved ontology and verified the required classes, properties, domains, ranges, and inherited applicability with RDFLib 7.6.0. All eight are covered at schema level under the interpretations recorded in Step 7. No ontology changes or individuals were added; no instance-level queries were executed. |
| 2 November 2026 | User approved the three-page report layout, supplied Yazdan ZandiyeVakili and student number 12642780, and requested DOCX and PDF using the documents and PDF skills. Created the report, complete hierarchy and selected preference-relationship diagrams, and five OWL examples. The final DOCX rendered to three pages; all page images were inspected and the matching PDF was placed in submission/. No files were uploaded or pushed. |
| 2 November 2026 | Applied Word Justify Low alignment to all 14 body paragraphs as requested, preserved other layout elements, and regenerated the matching PDF. All three rendered pages were visually checked; both files remain three pages. |
| 2 November 2026 | Italicized ontology identifiers, the namespace IRI, prefixed terms, datatype names, and the .owl extension in the report text and OWL table. Diagram class/property labels are also italic. Preserved the wording and all 14 Justify Low body paragraphs; inspected the final three-page DOCX render and regenerated the matching PDF. |
| 2 November 2026 | Extended italic formatting to technical tool/language names, including RDFLib, HermiT, Protégé, Codex, Turtle, RDF, RDFS, and OWL, while preserving italic ontology identifiers in the prose and table. Following the user clarification, restored regular text in both diagrams. Wording and Justify Low remain unchanged; all three rendered pages were inspected and the PDF refreshed. |
| 2 November 2026 | Added an AI usage section crediting the student with ontology creation and modeling decisions, Protégé inspection/validation, and AI help with the initial Turtle serialization and report writing/formatting. The report remains three pages after concise revisions to page 3. Inspected every rendered page and updated the Word report, submission PDF, and Desktop deliverables PDF. |
