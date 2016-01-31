The 'serial-1' directory contains AS relationships inferred using the method
described in "AS Relationships, Customer Cones, and Validation"
published in IMC 2013 (http://www.caida.org/publications/papers/2013/asrank/).

The as-rel files contain p2p and p2c relationships.  The format is:
<provider-as>|<customer-as>|-1
<peer-as>|<peer-as>|0

The ppdc-ases files contain the provider-peer customer cones inferred for
each AS.  Each line specifies an AS and all ASes we infer to be reachable
following a customer link.  The format is:
<cone-as> <customer-1-as> <customer-2-as> .. <customer-N-as>

------------------------
Acceptable Use Agreement
------------------------
 
The AUA that you accepted when you were given access to these datas is included
in pdf format as a separate file in the same directory as this README file.
When referencing this data (as required by the AUA), please use:

    The CAIDA AS Relationships Dataset, <date range used>
    http://www.caida.org/data/active/as-relationships/ 

Also, please, report your publication to CAIDA
(http://www.caida.org/data/publications/report-publication.xml).
