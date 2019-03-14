from scraper.factory import get_value


def get_result_by_mapping(content, data, mapSelectorValue):
    
    result = {}
    contentSpecific = content.select_one( mapSelectorValue.get('pathContainer')) if mapSelectorValue.get('pathContainer') else content
    fieldsToCreate = mapSelectorValue.get('fields')
    for key in fieldsToCreate.keys():
        field = fieldsToCreate.get(key)
        result[key] = get_value( field['type'], field['specification'], contentSpecific)
    result['url'] =  data.get('url')
    result['files'] = result['files'] if result.get('files') else  []
    return result
    






