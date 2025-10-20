import logging

logger = logging.getLogger(__name__)

def check_if_required_data_exists(payload, required):
    try:
        for field in required:
            if not payload.get(field, ""):
                return False  
        
        return True 
    
    except Exception as e:
        logger.info(f'An error occured during required data check: {e}')

def get_values_from_dict(dict, required_keys): 
    try: 
        new_dict = {}

        for key, value in dict.items():
            if  key in required_keys: 
                new_dict[key] = value

        return new_dict
    
    except Exception as e: 
        logger.info(f'An error occured while trying to get values from dict: {e}')