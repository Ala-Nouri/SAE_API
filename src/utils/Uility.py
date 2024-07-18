from src.models.Property import Property

def create_properties(properties,id):
    result = []
    for k,v in properties.items():
        if type(v) == str:
            result.append(Property(
                document_id = id,
                property_name = k,
                property_value = v))
        elif type(v) == list:
            for element in v:
                result = result + create_properties(element,id)
        else:
            result = result + create_properties(v,id)
    return result