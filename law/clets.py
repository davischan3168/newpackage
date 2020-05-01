#!/usr/bin/env python3
# -*-coding:utf-8-*-

from law.getGb import GBCase, GBJudicialDocument
from law.LawBJv1 import LawBJCase
from law.LawcaseChina import LawChinaCase
from law.LawCaseGuide import lawcaseII
from law.LawCaseSH_selenium import LawShSCase
from law.LawCICC import LawCICCase
from law.LawDXCaseGuide import DXLawcase
from law.LawGD import LawGDCase
from law.LawIterpretation import LawDocument, LawInterpretation
from law.SPPCaseGuide import SPPlawcase
from law.SPPIssue import SPPIssue

if __name__ == "__main__":
    print('Geting %s ....'%'公报')
    GBCase('http://gongbao.court.gov.cn/ArticleList.html?serial_no=al',2)
    print('Geting %s ....'%'公报判决书')
    GBJudicialDocument('http://gongbao.court.gov.cn/ArticleList.html?serial_no=cpwsxd',3)
    print('Geting %s ....'%'北京案例')
    LawBJCase(1)
    print('Geting %s ....'%'指导性案例')
    lawcaseII()
    urll='http://www.hshfy.sh.cn/shfy/gweb2017/channel_xw_list.jsp?pa=abG1kbT1MTTA2MDImbG1tYz2wuMD90dDO9gPdcssPdcssz&zd=spyj'
    url ='http://www.hshfy.sh.cn/shfy/gweb2017/channel_xw_list.jsp?pa=abG1kbT1MTTAxMDYmbG1tYz3C27C4y7W3qAPdcssPdcssz&zd=xwzx#'
    try:
        print('Geting %s ....'%'上海案例')
        LawShSCase(urll)
    except:
        print('Failed2 ...')
        pass
    try:
        print('Geting %s ....'%'上海案例1')
        LawShSCase(url)
    except:
        print('Failed1 ...')
        pass
    url='http://cicc.court.gov.cn/html/1//218/62/163/index.html'
    print('Geting %s ....'%'中国案例')
    LawCICCase(url)
    print('Geting %s ....'%'典型案例')
    DXLawcase()
    print('Geting %s ....'%'广东案例')
    LawGDCase(2)
    print('Geting %s ....'%'最高院司法文件')
    LawDocument()
    print('Geting %s ....'%'最高法司法解释')
    LawInterpretation()
    print('Geting %s ....'%'最高检案例')
    SPPlawcase()
    url='https://www.spp.gov.cn/spp/wsfbt/index.shtml'
    print('Geting %s ....'%'最高检司法文件')
    SPPIssue(url,2)    
    
