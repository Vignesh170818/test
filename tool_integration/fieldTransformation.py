import json,os
import logging

module_logger = logging.getLogger("tool_integration.fieldTransformation")

def mapJIRADictionaryTemplate(request_id,json_data,entityName,dataFlowDirection=''): 
    module_logger.info(f"Method 'mapDictionaryTemplate()' started. Request_Id: {request_id}")
    attribute_mapping = getEntityMapping(entityName) 
    if len(attribute_mapping) > 0:
        if (dataFlowDirection == 'inbound'):
            transformedOutput = { key: getattr(json_data.fields, value, None) for key, value in attribute_mapping.items()}
        else:
            common_keys = set(json_data.keys()) & set(attribute_mapping.keys())
            transformedOutput = {attribute_mapping.get(key, key): json_data[key] for key in common_keys}
    module_logger.info(f"Method 'mapDictionaryTemplate()' ended. Request_Id: {request_id}")
    return transformedOutput

def getEntityMapping(entityName):
    module_logger.info(f"Method 'getEntityMapping()' started")
    cwd = os.getcwd()
    json_file_path1 =  cwd + os.sep + "tool_integration"+ os.sep +"jsonTransform.json"
    with open(json_file_path1, 'r') as json_file1:
        data = json.load(json_file1)
        entity_attributes = data.get(entityName +'_mapping', [])
    module_logger.info(f"Method 'getEntityMapping()' ended")
    return entity_attributes

def mapHPALMDictionaryTemplate(request_id,json_data,entityName,parent_id): 
    module_logger.info(f"Method 'mapDictionaryTemplate()' started. Request_Id: {request_id}")
    attribute_mapping = getEntityMapping(entityName) 
    if len(attribute_mapping) > 0:
        common_keys = set(json_data.keys()) & set(attribute_mapping.keys())
        transformedOutput = {attribute_mapping.get(key, key): json_data[key] for key in common_keys}
        if transformedOutput:
            output_data_list = []
            transformedOutput["parent-id"] = parent_id if parent_id else "1001"
            if entityName == "test":
                transformedOutput["subtype-id"] = "Manual"
            for key, value in transformedOutput.items():
                    output_item = {
                        "Name": key,
                        "values": [
                            {
                                "value": value
                            }
                        ]
                    }
                    output_data_list.append(output_item)

            transformedOutput = {
                "Fields": output_data_list
            }
    module_logger.info(f"Method 'mapDictionaryTemplate()' ended. Request_Id: {request_id}")
    return transformedOutput