#!/usr/bin/env python3
# -*-coding:utf-8-*-

codeset={'A': 'A.N', 'AA': 'AA.N', 'AAPL': 'AAPL.OQ', 'AAXJ': 'AAXJ.OQ', 'ABAC': 'ABAC.OQ', 'ABT': 'ABT.N', 'ABX': 'ABX.N', 'ACH': 'ACH.N', 'ACXM': 'ACXM.OQ', 'ADBE': 'ADBE.OQ', 'ADI': 'ADI.OQ', 'ADS': 'ADS.N', 'ADSK': 'ADSK.OQ', 'AEP': 'AEP.N', 'AES': 'AES.N', 'AGQ': 'AGQ.AM', 'AIG': 'AIG.N', 'AKAM': 'AKAM.OQ', 'AL': 'AL.N', 'ALL': 'ALL.N', 'ALN': 'ALN.AM', 'AMAT': 'AMAT.OQ', 'AMBA': 'AMBA.OQ', 'AMCN': 'AMCN.OQ', 'AMD': 'AMD.OQ', 'AMGN': 'AMGN.OQ', 'AMRC': 'AMRC.N', 'AMZN': 'AMZN.OQ', 'APH': 'APH.N', 'ARRS': 'ARRS.OQ', 'ASHR': 'ASHR.AM', 'ASHS': 'ASHS.AM', 'ASX': 'ASX.N', 'ATHM': 'ATHM.N', 'ATI': 'ATI.N', 'ATSG': 'ATSG.OQ', 'ATV': 'ATV.N', 'ATVI': 'ATVI.OQ', 'AUO': 'AUO.N', 'AVG': 'AVG.N', 'AVGO': 'AVGO.OQ', 'AVP': 'AVP.N', 'AXP': 'AXP.N', 'B': 'B.N', 'BA': 'BA.N', 'BABA': 'BABA.N', 'BAC': 'BAC.N', 'BAX': 'BAX.N', 'BBRY': 'BBRY.OQ', 'BBY': 'BBY.N', 'BHP': 'BHP.N', 'BIDU': 'BIDU.OQ', 'BIIB': 'BIIB.OQ', 'BITA': 'BITA.N', 'BK': 'BK.N', 'BLDP': 'BLDP.OQ', 'BLK': 'BLK.N', 'BMY': 'BMY.N', 'BOX': 'BOX.N', 'BP': 'BP.N', 'BRCD': 'BRCD.OQ', 'BRK.A': 'BRK.A.N', 'BRK.B': 'BRK.B.N', 'BUD': 'BUD.N', 'BX': 'BX.N', 'BZUN': 'BZUN.OQ', 'C': 'C.N', 'CA': 'CA.OQ', 'CAAS': 'CAAS.OQ', 'CAF': 'CAF.N', 'CAJ': 'CAJ.N', 'CALI': 'CALI.OQ', 'CAT': 'CAT.N', 'CBAK': 'CBAK.OQ', 'CBPO': 'CBPO.OQ', 'CBS': 'CBS.N', 'CCCR': 'CCCR.OQ', 'CCIH': 'CCIH.OQ', 'CCM': 'CCM.N', 'CCRC': 'CCRC.OQ', 'CCU': 'CCU.N', 'CDNS': 'CDNS.OQ', 'CEA': 'CEA.N', 'CELG': 'CELG.OQ', 'CEO': 'CEO.N', 'CETC': 'CETC.OQ', 'CHA': 'CHA.N', 'CHAD': 'CHAD.AM', 'CHAU': 'CHAU.AM', 'CHL': 'CHL.N', 'CHNR': 'CHNR.OQ', 'CHT': 'CHT.N', 'CHU': 'CHU.N', 'CI': 'CI.N', 'CL': 'CL.N', 'CMCM': 'CMCM.N', 'CMCSA': 'CMCSA.OQ', 'CMG': 'CMG.N', 'CNET': 'CNET.OQ', 'CNIT': 'CNIT.OQ', 'CNTF': 'CNTF.OQ', 'CNXT': 'CNXT.AM', 'CNYA': 'CNYA.AM', 'CO': 'CO.N', 'COF': 'COF.N', 'COH': 'COH.N', 'COP': 'COP.N', 'COST': 'COST.OQ', 'CPB': 'CPB.N', 'CPHI': 'CPHI.AM', 'CREE': 'CREE.OQ', 'CRM': 'CRM.N', 'CSCO': 'CSCO.OQ', 'CSIQ': 'CSIQ.OQ', 'CTRP': 'CTRP.OQ', 'CTSH': 'CTSH.OQ', 'CTXS': 'CTXS.OQ', 'CVLT': 'CVLT.OQ', 'CVS': 'CVS.N', 'CVX': 'CVX.N', 'CXDC': 'CXDC.OQ', 'CY': 'CY.OQ', 'CYB': 'CYB.AM', 'CYBR': 'CYBR.OQ', 'CYD': 'CYD.N', 'CYOU': 'CYOU.OQ', 'D': 'D.N', 'DAL': 'DAL.N', 'DATA': 'DATA.N', 'DB': 'DB.N', 'DBA': 'DBA.AM', 'DBC': 'DBC.AM', 'DD': 'DD.N', 'DDD': 'DDD.N', 'DDM': 'DDM.AM', 'DGAZ': 'DGAZ.AM', 'DGP': 'DGP.AM', 'DGZ': 'DGZ.AM', 'DIA': 'DIA.AM', 'DIG': 'DIG.AM', 'DIS': 'DIS.N', 'DL': 'DL.N', 'DLB': 'DLB.N', 'DNR': 'DNR.N', 'DOG': 'DOG.AM', 'DOW': 'DOW.N', 'DQ': 'DQ.N', 'DRN': 'DRN.AM', 'DRV': 'DRV.AM', 'DTO': 'DTO.AM', 'DTV': 'DTV.N', 'DUG': 'DUG.AM', 'DUK': 'DUK.N', 'DUST': 'DUST.AM', 'DVA': 'DVA.N', 'DWT': 'DWT.AM', 'DXCM': 'DXCM.OQ', 'DXD': 'DXD.AM', 'DXJ': 'DXJ.AM', 'DZZ': 'DZZ.AM', 'E': 'E.N', 'EA': 'EA.OQ', 'EBAY': 'EBAY.OQ', 'EDC': 'EDC.AM', 'EDIT': 'EDIT.OQ', 'EDU': 'EDU.N', 'EEM': 'EEM.AM', 'EFA': 'EFA.AM', 'EHIC': 'EHIC.N', 'EL': 'EL.N', 'ENV': 'ENV.N', 'EQIX': 'EQIX.OQ', 'ERIC': 'ERIC.OQ', 'ERX': 'ERX.AM', 'ERY': 'ERY.AM', 'ETR': 'ETR.N', 'EUO': 'EUO.AM', 'EWA': 'EWA.AM', 'EWC': 'EWC.AM', 'EWD': 'EWD.AM', 'EWG': 'EWG.AM', 'EWH': 'EWH.AM', 'EWI': 'EWI.AM', 'EWJ': 'EWJ.AM', 'EWK': 'EWK.AM', 'EWM': 'EWM.AM', 'EWN': 'EWN.AM', 'EWO': 'EWO.AM', 'EWP': 'EWP.AM', 'EWQ': 'EWQ.AM', 'EWT': 'EWT.AM', 'EWU': 'EWU.AM', 'EWY': 'EWY.AM', 'EWZ': 'EWZ.AM', 'EXC': 'EXC.N', 'EXPE': 'EXPE.OQ', 'EZU': 'EZU.AM', 'F': 'F.N', 'FAS': 'FAS.AM', 'FAZ': 'FAZ.AM', 'FB': 'FB.OQ', 'FCEL': 'FCEL.OQ', 'FDX': 'FDX.N', 'FENG': 'FENG.N', 'FEYE': 'FEYE.OQ', 'FFIV': 'FFIV.OQ', 'FIT': 'FIT.N', 'FORK': 'FORK.OQ', 'FRI': 'FRI.AM', 'FSLR': 'FSLR.OQ', 'FTNT': 'FTNT.OQ', 'FXA': 'FXA.AM', 'FXC': 'FXC.AM', 'FXE': 'FXE.AM', 'FXF': 'FXF.AM', 'FXI': 'FXI.AM', 'FXP': 'FXP.AM', 'FXY': 'FXY.AM', 'GD': 'GD.N', 'GDOT': 'GDOT.N', 'GDX': 'GDX.AM', 'GDXJ': 'GDXJ.AM', 'GE': 'GE.N', 'GG': 'GG.N', 'GIGM': 'GIGM.OQ', 'GILD': 'GILD.OQ', 'GLD': 'GLD.AM', 'GLL': 'GLL.AM', 'GLUU': 'GLUU.OQ', 'GLW': 'GLW.N', 'GM': 'GM.N', 'GME': 'GME.N', 'GOGO': 'GOGO.OQ', 'GOOG': 'GOOG.OQ', 'GOOGL': 'GOOGL.OQ', 'GPRO': 'GPRO.OQ', 'GRPN': 'GRPN.OQ', 'GRUB': 'GRUB.N', 'GS': 'GS.N', 'GSH': 'GSH.N', 'GSK': 'GSK.N', 'GSOL': 'GSOL.OQ', 'H': 'H.N', 'HAL': 'HAL.N', 'HCM': 'HCM.OQ', 'HD': 'HD.N', 'HIG': 'HIG.N', 'HIMX': 'HIMX.OQ', 'HLF': 'HLF.N', 'HLG': 'HLG.OQ', 'HMC': 'HMC.N', 'HNP': 'HNP.N', 'HOLI': 'HOLI.OQ', 'HON': 'HON.N', 'HPQ': 'HPQ.N', 'HQCL': 'HQCL.OQ', 'HSBC': 'HSBC.N', 'HTHT': 'HTHT.OQ', 'IAU': 'IAU.AM', 'IBB': 'IBB.OQ', 'IBKR': 'IBKR.OQ', 'IBM': 'IBM.N', 'ICF': 'ICF.AM', 'ILMN': 'ILMN.OQ', 'INTC': 'INTC.OQ', 'INTU': 'INTU.OQ', 'IP': 'IP.N', 'IRBT': 'IRBT.OQ', 'ISRG': 'ISRG.OQ', 'ITB': 'ITB.AM', 'IVV': 'IVV.AM', 'IWM': 'IWM.AM', 'IWO': 'IWO.AM', 'IYF': 'IYF.AM', 'IYM': 'IYM.AM', 'IYR': 'IYR.AM', 'IYT': 'IYT.AM', 'IYZ': 'IYZ.AM', 'JASO': 'JASO.OQ', 'JBL': 'JBL.N', 'JCP': 'JCP.N', 'JD': 'JD.OQ', 'JKS': 'JKS.N', 'JMEI': 'JMEI.N', 'JNJ': 'JNJ.N', 'JNPR': 'JNPR.N', 'JOBS': 'JOBS.OQ', 'JPM': 'JPM.N', 'JRJC': 'JRJC.OQ', 'JUNO': 'JUNO.OQ', 'K': 'K.N', 'KANG': 'KANG.OQ', 'KBE': 'KBE.AM', 'KBSF': 'KBSF.OQ', 'KIE': 'KIE.AM', 'KITE': 'KITE.OQ', 'KLAC': 'KLAC.OQ', 'KNDI': 'KNDI.OQ', 'KO': 'KO.N', 'KORS': 'KORS.N', 'KWEB': 'KWEB.OQ', 'KWT': 'KWT.AM', 'KYO': 'KYO.N', 'KZ': 'KZ.OQ', 'LC': 'LC.N', 'LEJU': 'LEJU.N', 'LFC': 'LFC.N', 'LITB': 'LITB.N', 'LMT': 'LMT.N', 'LN': 'LN.N', 'LRCX': 'LRCX.OQ', 'LSCC': 'LSCC.OQ', 'LTBR': 'LTBR.OQ', 'LUV': 'LUV.N', 'LVS': 'LVS.N', 'M': 'M.N', 'MA': 'MA.N', 'MAT': 'MAT.OQ', 'MBLY': 'MBLY.N', 'MCD': 'MCD.N', 'MCHP': 'MCHP.OQ', 'MCO': 'MCO.N', 'MDSO': 'MDSO.OQ', 'MDT': 'MDT.N', 'MET': 'MET.N', 'MFG': 'MFG.N', 'MGM': 'MGM.N', 'MMI': 'MMI.N', 'MMM': 'MMM.N', 'MMYT': 'MMYT.OQ', 'MNKD': 'MNKD.OQ', 'MO': 'MO.N', 'MOMO': 'MOMO.OQ', 'MON': 'MON.N', 'MOO': 'MOO.AM', 'MPEL': 'MPEL.OQ', 'MRK': 'MRK.N', 'MRVL': 'MRVL.OQ', 'MS': 'MS.N', 'MSFT': 'MSFT.OQ', 'MSI': 'MSI.N', 'MTU': 'MTU.N', 'MU': 'MU.OQ', 'MXIM': 'MXIM.OQ', 'MXWL': 'MXWL.OQ', 'NCTY': 'NCTY.OQ', 'NDAQ': 'NDAQ.OQ', 'NFLX': 'NFLX.OQ', 'NHTC': 'NHTC.OQ', 'NKE': 'NKE.N', 'NLR': 'NLR.AM', 'NMR': 'NMR.N', 'NOAH': 'NOAH.N', 'NOK': 'NOK.N', 'NORD': 'NORD.N', 'NQ': 'NQ.N', 'NSC': 'NSC.N', 'NTAP': 'NTAP.OQ', 'NTES': 'NTES.OQ', 'NTP': 'NTP.N', 'NTT': 'NTT.N', 'NUAN': 'NUAN.OQ', 'NUGT': 'NUGT.AM', 'NUS': 'NUS.N', 'NVDA': 'NVDA.OQ', 'NVS': 'NVS.N', 'NWS': 'NWS.OQ', 'NXPI': 'NXPI.OQ', 'NYT': 'NYT.N', 'OIH': 'OIH.AM', 'OIIM': 'OIIM.OQ', 'OIL': 'OIL.AM', 'ORCL': 'ORCL.N', 'OSN': 'OSN.OQ', 'P': 'P.N', 'PANW': 'PANW.N', 'PBR': 'PBR.N', 'PCLN': 'PCLN.OQ', 'PEP': 'PEP.N', 'PFE': 'PFE.N', 'PG': 'PG.N', 'PGF': 'PGF.AM', 'PGJ': 'PGJ.OQ', 'PHG': 'PHG.N', 'PLUG': 'PLUG.OQ', 'PME': 'PME.OQ', 'PSQ': 'PSQ.AM', 'PTR': 'PTR.N', 'PYPL': 'PYPL.OQ', 'QCOM': 'QCOM.OQ', 'QID': 'QID.AM', 'QIWI': 'QIWI.OQ', 'QLD': 'QLD.AM', 'QQQ': 'QQQ.OQ', 'RACE': 'RACE.N', 'RENN': 'RENN.N', 'RF': 'RF.N', 'RHT': 'RHT.N', 'RIO': 'RIO.N', 'RJA': 'RJA.AM', 'RJI': 'RJI.AM', 'ROK': 'ROK.N', 'RP': 'RP.OQ', 'RSX': 'RSX.AM', 'RTH': 'RTH.AM', 'RTN': 'RTN.N', 'RUSL': 'RUSL.AM', 'RUSS': 'RUSS.AM', 'RWLK': 'RWLK.OQ', 'RWM': 'RWM.AM', 'S': 'S.N', 'SAP': 'SAP.N', 'SATS': 'SATS.OQ', 'SBUX': 'SBUX.OQ', 'SCO': 'SCO.AM', 'SDOW': 'SDOW.AM', 'SDS': 'SDS.AM', 'SFUN': 'SFUN.N', 'SGOC': 'SGOC.OQ', 'SH': 'SH.AM', 'SHAK': 'SHAK.N', 'SHI': 'SHI.N', 'SHOP': 'SHOP.N', 'SIMO': 'SIMO.OQ', 'SINA': 'SINA.OQ', 'SKF': 'SKF.AM', 'SLB': 'SLB.N', 'SLV': 'SLV.AM', 'SMFG': 'SMFG.N', 'SMH': 'SMH.AM', 'SMI': 'SMI.N', 'SMN': 'SMN.AM', 'SNE': 'SNE.N', 'SNP': 'SNP.N', 'SO': 'SO.N', 'SOHU': 'SOHU.OQ', 'SOL': 'SOL.N', 'SORL': 'SORL.OQ', 'SOXL': 'SOXL.AM', 'SPI': 'SPI.OQ', 'SPIL': 'SPIL.OQ', 'SPLK': 'SPLK.OQ', 'SPWR': 'SPWR.OQ', 'SPXU': 'SPXU.AM', 'SPY': 'SPY.AM', 'SQ': 'SQ.N', 'SQQQ': 'SQQQ.OQ', 'SRS': 'SRS.AM', 'SSO': 'SSO.AM', 'SSYS': 'SSYS.OQ', 'STX': 'STX.OQ', 'SVA': 'SVA.OQ', 'SVXY': 'SVXY.AM', 'SWFT': 'SWFT.N', 'SWKS': 'SWKS.OQ', 'SYMC': 'SYMC.OQ', 'SYNT': 'SYNT.OQ', 'T': 'T.N', 'TAL': 'TAL.N', 'TAN': 'TAN.AM', 'TCRD': 'TCRD.OQ', 'TDC': 'TDC.N', 'TEDU': 'TEDU.OQ', 'TER': 'TER.N', 'TGT': 'TGT.N', 'TIF': 'TIF.N', 'TM': 'TM.N', 'TNA': 'TNA.AM', 'TOUR': 'TOUR.OQ', 'TQQQ': 'TQQQ.OQ', 'TRI': 'TRI.N', 'TRIP': 'TRIP.OQ', 'TRMB': 'TRMB.OQ', 'TRUE': 'TRUE.OQ', 'TRV': 'TRV.N', 'TSLA': 'TSLA.OQ', 'TSM': 'TSM.N', 'TUR': 'TUR.OQ', 'TVIX': 'TVIX.OQ', 'TWM': 'TWM.AM', 'TWTR': 'TWTR.N', 'TWX': 'TWX.N', 'TXN': 'TXN.OQ', 'TYL': 'TYL.N', 'TZA': 'TZA.AM', 'UA': 'UA.N', 'UBS': 'UBS.N', 'UCO': 'UCO.AM', 'UDN': 'UDN.AM', 'UDOW': 'UDOW.AM', 'UGAZ': 'UGAZ.AM', 'UGL': 'UGL.AM', 'UMC': 'UMC.N', 'UNG': 'UNG.AM', 'UNH': 'UNH.N', 'UPRO': 'UPRO.AM', 'UPS': 'UPS.N', 'URE': 'URE.AM', 'USB': 'USB.N', 'USNA': 'USNA.N', 'USO': 'USO.AM', 'UTSI': 'UTSI.OQ', 'UTX': 'UTX.N', 'UUP': 'UUP.AM', 'UVXY': 'UVXY.AM', 'UWM': 'UWM.AM', 'UWT': 'UWT.AM', 'UYG': 'UYG.AM', 'UYM': 'UYM.AM', 'V': 'V.N', 'VALE': 'VALE.N', 'VEA': 'VEA.AM', 'VGK': 'VGK.AM', 'VIPS': 'VIPS.N', 'VIXY': 'VIXY.AM', 'VMW': 'VMW.N', 'VNET': 'VNET.OQ', 'VNQ': 'VNQ.AM', 'VOD': 'VOD.OQ', 'VRSN': 'VRSN.OQ', 'VRX': 'VRX.N', 'VWO': 'VWO.AM', 'VXX': 'VXX.AM', 'VXZ': 'VXZ.AM', 'VZ': 'VZ.N', 'W': 'W.N', 'WB': 'WB.OQ', 'WBAI': 'WBAI.N', 'WDAY': 'WDAY.N', 'WDC': 'WDC.OQ', 'WFC': 'WFC.N', 'WMB': 'WMB.N', 'WMT': 'WMT.N', 'WPZ': 'WPZ.N', 'WUBA': 'WUBA.N', 'WY': 'WY.N', 'WYNN': 'WYNN.OQ', 'X': 'X.N', 'XHB': 'XHB.AM', 'XIN': 'XIN.N', 'XIV': 'XIV.OQ', 'XLB': 'XLB.AM', 'XLE': 'XLE.AM', 'XLF': 'XLF.AM', 'XLI': 'XLI.AM', 'XLK': 'XLK.AM', 'XLNX': 'XLNX.OQ', 'XLP': 'XLP.AM', 'XLU': 'XLU.AM', 'XLV': 'XLV.AM', 'XLY': 'XLY.AM', 'XME': 'XME.AM', 'XNET': 'XNET.OQ', 'XOM': 'XOM.N', 'XONE': 'XONE.OQ', 'XPP': 'XPP.AM', 'XRT': 'XRT.AM', 'XRX': 'XRX.N', 'Y': 'Y.N', 'YANG': 'YANG.AM', 'YCS': 'YCS.AM', 'YECO': 'YECO.OQ', 'YELP': 'YELP.N', 'YGE': 'YGE.N', 'YIN': 'YIN.OQ', 'YINN': 'YINN.AM', 'YNDX': 'YNDX.OQ', 'YOD': 'YOD.OQ', 'YRD': 'YRD.N', 'YUM': 'YUM.N', 'YXI': 'YXI.AM', 'YY': 'YY.OQ', 'Z': 'Z.OQ', 'ZNGA': 'ZNGA.OQ', 'ZNH': 'ZNH.N', 'ZPIN': 'ZPIN.N', 'ZSL': 'ZSL.AM', 'ZX': 'ZX.N'}