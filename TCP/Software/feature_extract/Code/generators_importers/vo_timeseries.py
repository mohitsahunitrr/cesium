
vo_table_preamble = """
<?xml version="1.0"?>
<VOTABLE version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:noNamespaceSchemaLocation="http://www.ivoa.net/xml/VOTable/VOTable/v1.1">
  <COOSYS ID="J2000" equinox="J2000." epoch="J2000." system="eq_FK5"/>
"""

vo_timeseries_preamble = """<VOTIMESERIES version="0.01">\n"""
vo_timeseries_mjd = """<TIMESYS>
\t\t<TimeType ucd="frame.time.system?">MJD</TimeType>
\t\t<TimeZero ucd="frame.time.zero">0.0 </TimeZero>
\t\t<TimeSystem ucd="frame.time.scale">UTC</TimeSystem>
\t\t<TimeRefPos ucd="pos;frame.time">TOPOCENTER</TimeRefPos>
</TIMESYS>

"""

vo_source_preamble = """<?xml version="1.0"?>\n<VOSOURCE version="0.01">\n\t<COOSYS ID="J2000" equinox="J2000." epoch="J2000." system="eq_FK5"/>\n"""
