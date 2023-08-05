# -*- coding: utf-8 -*-
from XMLSortHelper import sort_xml_file, sort_xml_content
from ConvertXML2Obj import parse_xml_to_object

import json

xmlcontent2 = """
<people>
    <human att="2">
      <weight>中国</weight>
      <height>188</height>
    </human>
    <human att="1">
      <weight>74</weight>
      <height>187</height>
    </human>
</people>
"""

original_file = r"C:\Python27\Lib\site-packages\CodeLibWrapper\RobotFrameworkSample\SampleData\xmldiff_target.xml"
sorted_file = r"C:\Python27\Lib\site-packages\CodeLibWrapper\RobotFrameworkSample\SampleData\xmldiff_target_sorted.xml"
# sort_xml_file(original_file, sorted_file)

# xmlcontent1 = sort_xml_content(xmlcontent2)
# print xmlcontent1
obj = parse_xml_to_object(original_file)





# tree = xml.etree.ElementTree.fromstring(xmlcontent)
# myArray = [int(x.text) for x in tree.findall("human/weight")]
# print myArray
