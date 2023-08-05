"""Example data sets from real life.
"""
import csv
from pkg_resources import resource_filename

from quicktions import Fraction

from effectus.helpers import get_values, unfold_values

def get_data(filepath):
    """Read and unfold value-frequency mappings from file.

    Args:
        filepath: File path to source file.

    Returns:
        A list with unfolded values.
    """
    with open(resource_filename(__name__, filepath), 'r') as csvfile:
        reader = csv.reader(csvfile)
        vafreqs = get_values(reader)
        return unfold_values(vafreqs)

GERMAN_MOTORWAYS = tuple(get_data('csv/german_motorways.csv'))
"""Lengths of 120 German federal motorways (Autobahnen) in km.

Source: `Bundesanstalt für Straßenwesen`_, 2016.

.. _Bundesanstalt für Straßenwesen: http://www.bast.de
"""

GERMAN_HIGHWAYS = tuple(get_data('csv/german_highways.csv'))
"""Lengths of 393 German federal highways (Bundesstraßen) in km.

Source: `Bundesanstalt für Straßenwesen`_, 2016.

.. _Bundesanstalt für Straßenwesen: http://www.bast.de
"""

WKZS = tuple(get_data('csv/wkzs.csv'))
"""Area designated for wind power usage in ha in 315 of 396
municipalities of North Rhine Westphalia, Germany 2012-2016.
The remaining municipalities do not have designated any area
for wind power usage.

Source: State Office for Nature, Environment and Consumer
  Affairs of North-Rhine Westphalia (`LANUV`_) based on data
  of planning regions; municipalities mentioned below, 2016.
  The data may not be complete for some parts. Data state for
  planning regions Münster, Arnsberg und Köln: July 2015,
  Detmold: June 2015. RVR: Late 2014, Düsseldorf: January 2011.
  Municipalities Anröchte, Drensteinfurt, Drolshagen, Eslohe
  (Sauerland), Hemer, Kaarst, Lippstadt, Mettmann, Metelen,
  Warendorf, Wickede (Ruhr), Wülfrath: 2016.

.. _LANUV: http://lanuv.nrw.de
"""

SP500 = tuple(get_data('csv/sp500.csv'))
# pragma pylint: disable=line-too-long
"""Daily positive returns of S&P500 index from 1960 through 2015.

Negative returns have been replaced with zero.

Source: `Yahoo Finance`_, 2016.

.. _Yahoo Finance: http://finance.yahoo.com/quote/%5EGSPC/history?period1=-315622800&period2=1451516400&interval=1d&filter=history&frequency=1d
"""
# pragma pylint: enable=line-too-long

HOPEI_RAIN = tuple(get_data('csv/hopei_rain.csv'))
"""
Daily precipitation in mm on Hohenpeißenberg, Germany
(the world's oldest mountain weather station) from 1781 to 2015.

Source: `German Meteorological Office`, 2016.

.. _German Meteorological Office: http://www.dwd.de
"""

HOPEI_SUN = tuple(get_data('csv/hopei_sun.csv'))
"""
Daily sun hours on Hohenpeißenberg, Germany
(the world's oldest mountain weather station) from 1937 to 2015.

Source: `German Meteorological Office`, 2016.

.. _German Meteorological Office: http://www.dwd.de
"""

GERMAN_RIVERS = (1236, 1091, 866, 744, 524, 371, 300, 290, 256, 220, 219, 208,
                 188, 185, 182, 176, 169, 166, 165, 153, 153, 150, 143, 128,
                 124, 121, 118, 114, 107, 105, 105, 102, 101, 97, 97, 92, 91,
                 90, 80, 75, 73, 72, 72, 70, 68, 68, 67, 67, 65, 67, 63, 63,
                 62, 62, 61, 60, 60, 59, 59, 58, 57, 57, 57, 57, 57, 56, 55,
                 54, 52, 52, 52, 51, 50, 49, 49, 49, 48, 47, 47, 46, 45, 45,
                 45, 45, 45, 44, 43, 42, 42, 40, 40, 40, 40, 40, 40, 40, 39,
                 39, 38, 37, 37, 37, 36, 35, 35, 35, 35, 35, 35, 34, 34, 34,
                 34, 33, 33, 33, 33, 32, 31, 31, 31, 31, 30, 30, 30, 30, 30,
                 30, 30, 30, 30, 30, 29, 29, 29, 28, 28, 28, 28, 28, 28, 27,
                 27, 27, 27, 27, 26, 26, 26, 25, 25, 25, 25, 25, 25, 25, 25,
                 24, 24, 24, 24, 24, 23, 23, 23, 23, 23, 22, 22, 22, 22, 22,
                 22, 22, 22, 22, 22, 22, 22, 21, 21, 21, 21, 21, 21, 21, 21,
                 21, 20, 20, 20, 20, 20, 19, 18, 18, 18, 18, 18, 18, 18, 18,
                 17, 17, 17, 17, 17, 17, 16, 16, 16, 16, 16, 16, 16, 16, 16,
                 16, 16, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 14, 14,
                 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12, 12, 12,
                 12, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
                 11, 10, 10, 10, 10)
# pragma pylint: disable=line-too-long
"""Lengths of 267 longest German rivers in km.
Source: `Wikipedia`_

.. _Wikipedia: https://de.wikipedia.org/w/index.php?title=Liste_von_Flüssen_in_Deutschland&oldid=158665390
"""
# pragma pylint: enable=line-too-long

MISSING_TEETH = get_data('csv/missing_teeth.csv')
"""Number of missing teeth of 966 young German adults (35 to 44 years).

Source: `Institute of German Dentists, Cologne`_: Fifth German Oral Health Study
(DMS V), ISBN 978-3-7691-0020-4.

.. _Institute of German Dentists, Cologne: http://www.idz-koeln.de
"""

BOXOFFICE = tuple(get_data('csv/boxoffice.csv'))
"""Boxoffice revenue of 4,189 movies in US Dollars.

Source: `OMDb`_.

.. _OMDb: https://github.com/rstudio/shiny-examples/tree/master/051-movie-explorer
"""
BELLS = tuple(get_data('csv/bells.csv'))
"""Weights of 9,605 church bells in kg of the German
archbishoprics of `Cologne`_, `Aachen`_ and `Essen`_.

.. _Cologne: http://glockenbuecherebk.de
.. _Aachen: http://www.glockenbuecherbaac.de
.. _Essen: http://www.glockenbuecherbes.de
"""

WOMEN_INTERCOURSE = tuple(get_data('csv/women_intercourse.csv'))
"""Number of vaginal sex partners of 11,110 women.

Source: Jakob Pastötter, Nicolas Drey, Anthony Pryce: Sex Study 2008 - Sexual
Behaviour in Germany. DGSS and City University London.
"""

GERMAN_MOTORWAYS_RELATIONS = \
[(Fraction(1, 120), Fraction(845480461294633, 11361209669344296)),
 (Fraction(1, 60), Fraction(1902484969540813, 14201512086680370)),
 (Fraction(1, 40), Fraction(2723270399675597, 14201512086680370)),
 (Fraction(1, 30), Fraction(186709291192229, 788972893704465)),
 (Fraction(1, 24), Fraction(146027360964517, 525981929136310)),
 (Fraction(1, 20), Fraction(8995764333812123, 28403024173360740)),
 (Fraction(7, 120), Fraction(55882067641922, 157794578740893)),
 (Fraction(1, 15), Fraction(5549674990036583, 14201512086680370)),
 (Fraction(3, 40), Fraction(2011336620690637, 4733837362226790)),
 (Fraction(1, 12), Fraction(3206835613571482, 7100756043340185)),
 (Fraction(11, 120), Fraction(3381657962387866, 7100756043340185)),
 (Fraction(1, 10), Fraction(1412652539366605, 2840302417336074)),
 (Fraction(13, 120), Fraction(1226908375047646, 2366918681113395)),
 (Fraction(7, 60), Fraction(2552149740006059, 4733837362226790)),
 (Fraction(1, 8), Fraction(1587562849113211, 2840302417336074)),
 (Fraction(2, 15), Fraction(4106730905324749, 7100756043340185)),
 (Fraction(17, 120), Fraction(471000239349578, 788972893704465)),
 (Fraction(3, 20), Fraction(4369569159944602, 7100756043340185)),
 (Fraction(19, 120), Fraction(1496838479666654, 2366918681113395)),
 (Fraction(1, 6), Fraction(512366310145684, 788972893704465)),
 (Fraction(7, 40), Fraction(943567893608530, 1420151208668037)),
 (Fraction(11, 60), Fraction(1604169139731388, 2366918681113395)),
 (Fraction(23, 120), Fraction(4903931811043738, 7100756043340185)),
 (Fraction(1, 5), Fraction(36984720572683, 52598192913631)),
 (Fraction(5, 24), Fraction(1015398988251136, 1420151208668037)),
 (Fraction(13, 60), Fraction(5160063044734157, 7100756043340185)),
 (Fraction(9, 40), Fraction(1047515722898473, 1420151208668037)),
 (Fraction(7, 30), Fraction(5311410820297523, 7100756043340185)),
 (Fraction(29, 120), Fraction(1076465864057815, 1420151208668037)),
 (Fraction(1, 4), Fraction(5450169187722854, 7100756043340185)),
 (Fraction(31, 120), Fraction(5517954079575244, 7100756043340185)),
 (Fraction(4, 15), Fraction(372272646932398, 473383736222679)),
 (Fraction(11, 40), Fraction(5647861378396978, 7100756043340185)),
 (Fraction(17, 60), Fraction(5708499444668824, 7100756043340185)),
 (Fraction(7, 24), Fraction(5768972584196504, 7100756043340185)),
 (Fraction(3, 10), Fraction(5823123531864472, 7100756043340185)),
 (Fraction(37, 120), Fraction(1175223998464655, 1420151208668037)),
 (Fraction(19, 60), Fraction(5928896550456523, 7100756043340185)),
 (Fraction(13, 40), Fraction(5980738523706161, 7100756043340185)),
 (Fraction(1, 3), Fraction(6031371034165246, 7100756043340185)),
 (Fraction(41, 120), Fraction(6081508764391832, 7100756043340185)),
 (Fraction(7, 20), Fraction(1226120391714406, 1420151208668037)),
 (Fraction(43, 120), Fraction(6175242130659736, 7100756043340185)),
 (Fraction(11, 30), Fraction(46070351656872, 52598192913631)),
 (Fraction(3, 8), Fraction(6262213500416818, 7100756043340185)),
 (Fraction(23, 60), Fraction(2100232135796326, 2366918681113395)),
 (Fraction(47, 120), Fraction(422604624213224, 473383736222679)),
 (Fraction(2, 5), Fraction(141687955073561, 157794578740893)),
 (Fraction(49, 120), Fraction(6412186886445464, 7100756043340185)),
 (Fraction(5, 12), Fraction(1289485246823137, 1420151208668037)),
 (Fraction(17, 40), Fraction(1295994355659571, 1420151208668037)),
 (Fraction(13, 30), Fraction(6512077517828914, 7100756043340185)),
 (Fraction(53, 120), Fraction(6544073306197196, 7100756043340185)),
 (Fraction(9, 20), Fraction(6576014118984089, 7100756043340185)),
 (Fraction(11, 24), Fraction(6607515127119871, 7100756043340185)),
 (Fraction(7, 15), Fraction(2212235720279108, 2366918681113395)),
 (Fraction(19, 40), Fraction(1332322219841290, 1420151208668037)),
 (Fraction(29, 60), Fraction(1337270022166282, 1420151208668037)),
 (Fraction(59, 120), Fraction(6710704293386648, 7100756043340185)),
 (Fraction(1, 2), Fraction(6731265160826059, 7100756043340185)),
 (Fraction(61, 120), Fraction(6750506614312139, 7100756043340185)),
 (Fraction(31, 60), Fraction(6767604020124056, 7100756043340185)),
 (Fraction(21, 40), Fraction(2260907435001992, 2366918681113395)),
 (Fraction(8, 15), Fraction(6796576151515954, 7100756043340185)),
 (Fraction(13, 24), Fraction(252203533820086, 262990964568155)),
 (Fraction(11, 20), Fraction(6821919894536191, 7100756043340185)),
 (Fraction(67, 120), Fraction(6833244864302284, 7100756043340185)),
 (Fraction(17, 30), Fraction(6844459882905599, 7100756043340185)),
 (Fraction(23, 40), Fraction(1371080004720394, 1420151208668037)),
 (Fraction(7, 12), Fraction(6865900359647231, 7100756043340185)),
 (Fraction(71, 120), Fraction(6876400695692492, 7100756043340185)),
 (Fraction(3, 5), Fraction(6886516202668031, 7100756043340185)),
 (Fraction(73, 120), Fraction(1379326341928714, 1420151208668037)),
 (Fraction(37, 60), Fraction(2301845917942852, 2366918681113395)),
 (Fraction(5, 8), Fraction(6914113944525209, 7100756043340185)),
 (Fraction(19, 30), Fraction(2307270175306547, 2366918681113395)),
 (Fraction(77, 120), Fraction(769939125748076, 788972893704465)),
 (Fraction(13, 20), Fraction(1387396757276590, 1420151208668037)),
 (Fraction(79, 120), Fraction(6944515441033216, 7100756043340185)),
 (Fraction(2, 3), Fraction(6951772217776538, 7100756043340185)),
 (Fraction(27, 40), Fraction(154645088767108, 157794578740893)),
 (Fraction(41, 60), Fraction(2322003631118746, 2366918681113395)),
 (Fraction(83, 120), Fraction(6972882841029838, 7100756043340185)),
 (Fraction(7, 10), Fraction(6979369959633716, 7100756043340185)),
 (Fraction(17, 24), Fraction(6985747127074817, 7100756043340185)),
 (Fraction(43, 60), Fraction(466134289556876, 473383736222679)),
 (Fraction(29, 40), Fraction(6998116632887297, 7100756043340185)),
 (Fraction(11, 15), Fraction(7003889068933121, 7100756043340185)),
 (Fraction(89, 120), Fraction(7009606529397556, 7100756043340185)),
 (Fraction(3, 4), Fraction(2338368029178812, 2366918681113395)),
 (Fraction(91, 120), Fraction(2340163898170846, 2366918681113395)),
 (Fraction(23, 30), Fraction(7025384521256141, 7100756043340185)),
 (Fraction(31, 40), Fraction(52075721277173, 52598192913631)),
 (Fraction(47, 60), Fraction(7035005247999181, 7100756043340185)),
 (Fraction(19, 24), Fraction(2346559390805743, 2366918681113395)),
 (Fraction(4, 5), Fraction(7044131194509722, 7100756043340185)),
 (Fraction(97, 120), Fraction(2349308169875183, 2366918681113395)),
 (Fraction(49, 60), Fraction(1410310579599442, 1420151208668037)),
 (Fraction(33, 40), Fraction(470301438626147, 473383736222679)),
 (Fraction(5, 6), Fraction(1411498052157440, 1420151208668037)),
 (Fraction(101, 120), Fraction(2353431338479343, 2366918681113395)),
 (Fraction(17, 20), Fraction(7063097770088858, 7100756043340185)),
 (Fraction(103, 120), Fraction(1413147319599104, 1420151208668037)),
 (Fraction(13, 15), Fraction(2356125141967394, 2366918681113395)),
 (Fraction(7, 8), Fraction(7071014253808844, 7100756043340185)),
 (Fraction(53, 60), Fraction(7073598106134118, 7100756043340185)),
 (Fraction(107, 120), Fraction(7076126982878003, 7100756043340185)),
 (Fraction(9, 10), Fraction(2359551953207296, 2366918681113395)),
 (Fraction(109, 120), Fraction(1416214957040599, 1420151208668037)),
 (Fraction(11, 12), Fraction(787048748355857, 788972893704465)),
 (Fraction(37, 40), Fraction(1417127551691653, 1420151208668037)),
 (Fraction(14, 15), Fraction(7087726830551039, 7100756043340185)),
 (Fraction(113, 120), Fraction(7089815902643813, 7100756043340185)),
 (Fraction(19, 20), Fraction(7091904974736587, 7100756043340185)),
 (Fraction(23, 24), Fraction(7093774144503806, 7100756043340185)),
 (Fraction(29, 30), Fraction(7095588338689636, 7100756043340185)),
 (Fraction(39, 40), Fraction(2365782519098026, 2366918681113395)),
 (Fraction(59, 60), Fraction(473240799711068, 473383736222679)),
 (Fraction(119, 120), Fraction(2366607152818858, 2366918681113395)),
 (Fraction(1, 1), Fraction(7100756043340184, 7100756043340185))]
