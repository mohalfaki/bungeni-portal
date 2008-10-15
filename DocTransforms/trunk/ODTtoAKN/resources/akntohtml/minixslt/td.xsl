<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:akn="http://www.akomantoso.org/1.0"
    xmlns="http://www.akomantoso.org/1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
    <xsl:output indent="yes" method="xhtml" encoding="UTF-8"/>

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="akn:*">
        <xsl:element name="{node-name(.)}">
            <xsl:for-each select="@*">
                <xsl:attribute name="{name(.)}">
                    <xsl:value-of select="."/>
                </xsl:attribute>
            </xsl:for-each>
            <xsl:apply-templates />
        </xsl:element>
    </xsl:template>

    <xsl:template match="akn:td">
        <td>
            <xsl:attribute name="class">html_table_column</xsl:attribute>
			<xsl:attribute name="colspan" select="@colspan" />
			<xsl:attribute name="rowspan" select="@rowspan" />

            <xsl:apply-templates />
        </td>
    </xsl:template>
    
    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template> 

</xsl:stylesheet>
