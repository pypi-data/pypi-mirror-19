# -*- coding: utf-8 -*-
from __future__ import print_function
from deepdiff import DeepDiff  # For Deep Difference of 2 objects
import xml.etree.ElementTree
from pprint import pprint
from CodeLibWrapper.XMLFunction.ConvertXML2Obj import parse_xml_to_object
import collections
import re
import sys
from lxml import etree
from operator import itemgetter
from pprint import pprint as pp


def sort(tree):
    root = tree.getroot()

    # Sort child elements by tag (what I think of as name) first
    for parent in root.xpath('//*[./*]'):
        parent[:] = sorted(parent, key=lambda x: x.tag)

    # The child elements of the root are already ordered by tag. Now order each
    # element with the same tag (e.g., script-group, job-config, etc) by ID.
    element_list = []

    for elem in root.iterchildren():
        tmp_tag = elem.tag
        tmp_attr = int(elem.attrib.get('id'))
        elem_str = etree.tostring(elem)
        element_list.append((tmp_tag, tmp_attr, elem_str))

    # Get things in sorted order, then print only the last part of the tuple with
    # the XML string. key=itemgetter() does a two-level sort, first by element
    # name, and then by id. decode() produces raw ASCII from a binary string.
    for elem_str in sorted(element_list, key=itemgetter(0, 1)):
        print(elem_str[2].decode('ascii'))


# region    xml_content
xml_content = """
<StockExchangeSecurities>
    <MessageInfo>
        <MessageCode>200</MessageCode>
        <MessageDetail>Request data successfully</MessageDetail>
    </MessageInfo>
    <GeneralInfo>
        <CIK>917851</CIK>
        <CUSIP>91912E204</CUSIP>
        <CompanyName>Vale SA</CompanyName>
        <ExchangeId>PAR</ExchangeId>
        <ISIN>US91912E2046</ISIN>
        <SEDOL>2933900</SEDOL>
        <Symbol>VALE5</Symbol>
    </GeneralInfo>
    <StockExchangeSecurityEntityList>
        <StockExchangeSecurityEntity>
            <CIK>917851</CIK>
            <CUSIP>91912E204</CUSIP>
            <CompanyName>Vale SA</CompanyName>
            <ExchangeId>PAR</ExchangeId>
            <ISIN>US91912E2046</ISIN>
            <InvestmentTypeId>PE</InvestmentTypeId>
            <SEDOL>2933900</SEDOL>
            <StockStatus>1</StockStatus>
            <Symbol>VALE5</Symbol>
        </StockExchangeSecurityEntity>
    </StockExchangeSecurityEntityList>
</StockExchangeSecurities>"""
# endregion

# region    xml_content2
xml_content2 = """
    <StockExchangeSecurities>
    <MessageInfo>
        <MessageCode>200</MessageCode>
        <MessageDetail>Request data successfully</MessageDetail>
    </MessageInfo>
    <GeneralInfo>
        <CIK>917851</CIK>
        <CUSIP>91912E204</CUSIP>
        <CompanyName>Vale SA</CompanyName>
        <ExchangeId>PAR</ExchangeId>
        <ISIN>US91912E2046</ISIN>
        <SEDOL>2933900</SEDOL>
        <Symbol>VALE5</Symbol>
    </GeneralInfo>
    <StockExchangeSecurityEntityList>
        <StockExchangeSecurityEntity>
            <CompanyName>International Business Machines Corp</CompanyName>
            <ExchangeId>NYS</ExchangeId>
            <Symbol>IBM</Symbol>
            <CUSIP>459200101</CUSIP>
            <CIK>51143</CIK>
            <ISIN>US4592001014</ISIN>
            <SEDOL>2005973</SEDOL>
            <InvestmentTypeId>EQ</InvestmentTypeId>
            <StockStatus>Active</StockStatus>
        </StockExchangeSecurityEntity>
    </StockExchangeSecurityEntityList>
</StockExchangeSecurities>
    """
# endregion

#  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://equityapi.morningstar.com/"


tree1 = xml.etree.ElementTree.fromstring(xml_content)
tree2 = xml.etree.ElementTree.fromstring(xml_content2)
ddiff = DeepDiff(tree1, tree2,report_repetition=True, ignore_order=True)


# doc1 = parse_xml_to_object(xml_content)
# doc2 = parse_xml_to_object(xml_content2)
# ddiff = DeepDiff(doc1, doc2,report_repetition=True, ignore_order=True)

pprint(ddiff)
