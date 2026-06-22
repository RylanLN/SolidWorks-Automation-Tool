def getProperties(model):
    # show list of custom properties associated with active part, assembly, or drawing
    modelExt = model.Extension
    p = modelExt.CustomPropertyManager("")
    properties = p.GetNames
    return properties


def updateProperty(model, propertyName: str, Value: str):
    # update value of custom property associated with active part, assembly, or drawing
    modelExt = model.Extension
    p = modelExt.CustomPropertyManager("")

    # add or update property
    # add3 creates property if it doesn't exist, or updates it if it does
    p.Add3(propertyName, 30, Value, 1)

    model.EditRebuild3
