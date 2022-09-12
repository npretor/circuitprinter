from dxfOperations import GetDXFPolygons


inst = GetDXFPolygons('testPrint1.dxf')

polygonArray = inst.parseToArray()
print(polygonArray)

