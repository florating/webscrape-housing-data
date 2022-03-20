# UCI Housing Info

The multi-page PDF for Palo Verde: [click here](./data/palo-verde-pdfs/v2/palo_verde-all_plans_v2.pdf)

The multi-page PDF for Verona Place: [click here](./data/verano-place-pdfs/v2/verano_place-all_plans_v2.pdf)

## Instructions

To run the script yourself:

- `virtualenv env`
- `env source/bin/activate`
- `pip install -r requirements.txt`
- Webscrape for table info: `python3 main.py`
- Download PDF files, add table info to each individual PDF file, then merge into a multi-page PDF file: `python3 pdf_merger.py`
  - Be sure to follow the user prompts carefully!
- `deactivate` when you are done

You may want to add a rate limiter if you end up trying this with more websites.

- eg: https://pypi.org/project/ratelimit/

## Resources

### Webpages

- https://housing.uci.edu/campus-village/
- https://housing.uci.edu/palo-verde/
- https://housing.uci.edu/verano-place/

### Web Scraping

- https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- https://pypi.org/project/selenium/
- https://towardsdatascience.com/17-terminal-commands-every-programmer-should-know-4fc4f4a5e20e

### PDF Manipulation

- https://realpython.com/creating-modifying-pdf/#concatenating-and-merging-pdfs
- https://stackoverflow.com/questions/1180115/add-text-to-existing-pdf-using-python

**Unused:**

- https://pyfpdf.readthedocs.io/en/latest/
