def parse_dataype(datatype_str):
    if datatype_str[0].lower() == "h":
        return "hum"
    elif datatype_str[0].lower() == "t":
        return "temp"
    else: 
        raise ValueError(f"Invalid datatype {datatype_str}")
    
opop = parse_dataype("Temperdfdf")

print(opop)