#Scraper based in configuration per webpage

##Libraries used
requests
bs4
urllib.parse
dateparser
datetime

##Configuration per webpage

###config --> GeneralScraper(url, configObject)
for fields boolean, if no there is, by default is False
config is a dictionary whit this possibles fields:

#### hasCategories

'hasCategories': True | False
indicate if the webpage has categories, by samples 'ages' ( see: https://www.anepe.cl/centro-de-estudios-estrategicos-2/ciee-cuadernos-de-trabajo-2017/),
authors ( https://www.df.cl/opinion)

#### theRootUrlIsACategory

'theRootUrlIsACategory': True | False
Indicate si the first url is also a category

#### selectorCategories

'selectorCategories': String
Is a selector css that wrapper the categories area htmml

#### hasItems

'hasItems': True | False
Indicate if the webpage is a conteiner of items as news, publications

#### selectorItems

'selectorItems': string
Is a selector css that identify each item

#### hasPagination

'hasPagination': True | False
Indicate if the webpage has pagination

#### selectorPagination

'selectorItems': string
Is a selector css that identify pagination area html

###set_map_selector_values()
s = GeneralScraper(url, {
'hasPagination': True,
'hasItems': True,
'selectorItems': '.td_module_19',
'selectorPagination': '.page-nav' }, header )
s.set_map_selector_values({
'pathContainer':'.td-ss-main-content',
'fields': {
'title': {'type': 'text', 'specification' : { 'path':'h1' }},
'description': {'type': 'paragraph', 'specification' : { 'path':'p'}},
'date': {'type': 'date', 'specification' : { 'path':'time','value':'datetime' }},
'autor': {'type': 'text', 'specification' : { 'path':'.author > span' }}
}
})
####pathContainer
the css selector that wrapping the area to scrape inside webpage, is used to delimited area html to scrape

#### fields

each field has type and specification attributes
in different files inside webpages there are samples
