from final_project_risk_analysis import risk_analysis


bank_list=['Citizen Bank','Civil Bank','Everest Bank','Global Bank','Investment Bank','Kumari Bank','Laxmi Bank','Machapuchre Bank','Nepal Bank Limited','Nic Asia Bank','NMB Bank','Prabhu Bank','Prime Bank','Sanima Bank','SBI Bank','Siddhartha Bank','Sunrise Bank'];
quarterlist = [
    'Q1 2064', 'Q2 2064', 'Q3 2064', 'Q4 2064',
    'Q1 2065', 'Q2 2065', 'Q3 2065', 'Q4 2065',
    'Q1 2066', 'Q2 2066', 'Q3 2066', 'Q4 2066',
    'Q1 2067', 'Q2 2067', 'Q3 2067', 'Q4 2067',
    'Q1 2068', 'Q2 2068', 'Q3 2068', 'Q4 2068',
    'Q1 2069', 'Q2 2069', 'Q3 2069', 'Q4 2069',
    'Q1 2070', 'Q2 2070', 'Q3 2070', 'Q4 2070',
    'Q1 2071', 'Q2 2071', 'Q3 2071', 'Q4 2071',
    'Q1 2072', 'Q2 2072', 'Q3 2072', 'Q4 2072',
    'Q1 2073', 'Q2 2073', 'Q3 2073', 'Q4 2073',
    'Q1 2074', 'Q2 2074', 'Q3 2074', 'Q4 2074',
    'Q1 2075', 'Q2 2075', 'Q3 2075', 'Q4 2075',
    'Q1 2076', 'Q2 2076', 'Q3 2076', 'Q4 2076',
    'Q1 2077', 'Q2 2077', 'Q3 2077', 'Q4 2077',
    'Q1 2078', 'Q2 2078', 'Q3 2078', 'Q4 2078',
    'Q1 2079', 'Q2 2079', 'Q3 2079', 'Q4 2079',
    'Q1 2080', 'Q2 2080', 'Q3 2080', 'Q4 2080'
];
financial_metrics = [
    "reserves",
    "debenture and bond",
    "borrowings",
    "deposits",
    "income tax liability",
    "total assets",
    "loan and advancements",
    "interest income",
    "interest expense",
    "net interest income",
    "net fee and commission income",
    "total operating income",
    "staff expenses",
    "operating profit",
    "non operating income expense",
    "profit for the period",
    "capital fund to rwa",
    "non performing loan to total loan",
    "total loan loss provision to npl",
    "cost of fund",
    "net interest spread",
    "return on equity",
    "return on total assets",
    "credit to deposit ratio",
    "base rate",
    "market share price",
    "other liabilities",
    "debt ratio",
    "interest income to assets ratio",
    "interest income margin",
    "return on investment",
    "commission to operating income",
    "staff expense to income ratio",
    "net profit margin",
    "income tax portion of operating profit",
    "loan to deposit ratio"
]



def normalize(banklist,quarterlist):
    x=0
    maxfirst = -100
    minfirst = 100
    maxsecond = -100
    minsecond = 100
    maxthird = -100
    minthird = 100
    for bank in banklist:
        for quarter in quarterlist:
            x=x+1

            a=risk_analysis(datafile='D:/python tesseract/z score/3d_zscore_table.csv',quarter=quarter,bank=bank)
            print(a[0])
            if a[0]!=None:
                if a[0]>maxfirst:
                    maxfirst=a[0]
            if a[0]!=None:
                if a[0]<minfirst:
                    minfirst=a[0]
            if a[1]!=None:
                if a[1]>maxsecond:
                    maxsecond=a[1]
            if a[1]!=None:
                if a[1]<minsecond:
                    minsecond=a[1]
            if a[2]!=None:
                if a[2]>maxthird:
                    maxthird=a[2]
            if a[2]!=None:
                if a[2]<minthird:
                    minthird=a[2]

    print("maxfirst=",maxfirst)
    print("minfirst=", minfirst)
    print("maxsecond=", maxsecond)
    print("minsecond=", minsecond)
    print("maxthird=", maxthird)
    print("minthird=", minthird)
    print(x)

#normalize(banklist=bank_list,quarterlist=quarterlist)

#maxfirst= 0.953690214839989
#minfirst= -1.0000000000000002
#maxsecond= 0.8820812056064548
#minsecond= -0.8978659288706474
#maxthird= 0.8623360470815973
#minthird= -0.9907139822450888