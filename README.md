<a className="gh-badge" href="https://datahub.io/core/investor-flow-of-funds-us"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Monthly net new cash flow by US investors into various mutual fund investment
classes (equities, bonds etc). Statistics come from the Investment Company
Institute (ICI).

## Data

The earliest data comes from 2007 up until today.
Data comes from the data provided on the [ICI Statistics pages][ici], in
particular:

* Summary: Estimated Long-Term Mutual Fund Flows Data (xls)

[ici]: http://www.ici.org/research/stats

Notes for Long-Term Mutual Fund Flows Data:

* All figures are (nominal) millions of US dollars (USD)
* Weekly cash flows are estimates based on reporting covering 98 percent of
  industry assets, while monthly flows are actual numbers as reported in ICI's
  "Trends in Mutual Fund Investing."

## Preparation

Run the python script:

Install the requirements   
```  
pip install -r scripts/requirements.txt
```
Now run the script    
```
python scripts/process.py
```    

## Automation

Up-to-date (auto-updates every month) investor-flow-of-funds dataset could be found on the datahub.io: https://datahub.io/core/investor-flow-of-funds-us

## License

This Data Package is licensed by its maintainers under the [Public Domain Dedication and License (PDDL)](http://opendatacommons.org/licenses/pddl/1.0/).