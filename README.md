Monthly net new cash flow by US investors into various mutual fund investment
classes (equities, bonds etc). Statistics come from the Investment Company
Institute (ICI).

## Data

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

  # Install the requirements    
  pip install -r scripts/requirements.txt
  # Now run the script    
  python scripts/process.py
    
