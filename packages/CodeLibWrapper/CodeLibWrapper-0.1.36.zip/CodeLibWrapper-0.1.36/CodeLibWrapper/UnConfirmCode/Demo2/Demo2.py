# -*- coding: utf-8 -*-
from pyxmldiff import xmldiff


DEFAULT_NAMESPACES = {"office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",}

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
           <StockExchangeSecurityEntity>
            <CompanyName>International Business Machines Corp</CompanyName>
            <ExchangeId>NYS</ExchangeId>
            <Symbol>IBM</Symbol>
            <CUSIP>459200102</CUSIP>
            <CIK>51144</CIK>
            <ISIN>US4592001015</ISIN>
            <SEDOL>2005976</SEDOL>
            <InvestmentTypeId>EQA</InvestmentTypeId>
            <StockStatus>Active1</StockStatus>
        </StockExchangeSecurityEntity>
    </StockExchangeSecurityEntityList>
</StockExchangeSecurities>
    """
# endregion


def main():
    A = xmldiff.fromstring(xml_content)
    B = xmldiff.fromstring(xml_content2)

    xmldiff.xmlDiff(A, B, namespaces=DEFAULT_NAMESPACES)


if __name__ == '__main__':
    main()