
from __future__ import print_function
from __future__ import absolute_import

from .securityhandlerhelper import securityhandlerhelper
import re as re

dateTimeFormat = '%Y-%m-%d %H:%M'
import arcrest

from . import featureservicetools as featureservicetools

from arcrest.hostedservice import AdminFeatureService
import datetime, time
import json
import os
import arcresthelper.common as common
import gc
import sys

from .packages.six.moves import urllib_parse as urlparse

try:
    import pyparsing
    pyparsingInstall = True
    from arcresthelper import select_parser
except:
    pyparsingInstall = False

import inspect

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno
#----------------------------------------------------------------------
def trace():
    """Determines information about where an error was thrown.

    Returns:
        tuple: line number, filename, error message
    Examples:
        >>> try:
        ...     1/0
        ... except:
        ...     print("Error on '{}'\\nin file '{}'\\nwith error '{}'".format(*trace()))
        ...        
        Error on 'line 1234'
        in file 'C:\\foo\\baz.py'
        with error 'ZeroDivisionError: integer division or modulo by zero'

    """
    import traceback, inspect, sys
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    filename = inspect.getfile(inspect.currentframe())
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror


class publishingtools(securityhandlerhelper):
    #----------------------------------------------------------------------
    def getItemID(self, userContent, title=None, name=None, itemType=None):
        """Gets the ID of an item by a combination of title, name, and type.
        
        Args:
            userContent (list): A list of user content.
            title (str): The title of the item. Defaults to ``None``.
            name (str): The name of the item. Defaults to ``None``.
            itemType (str): The type of the item. Defaults to ``None``.
        Returns:
            str: The item's ID. If the item does not exist, ``None``.        
        Raises:
            AttributeError: If both ``title`` and ``name`` are not specified (``None``).
        See Also:
            :py:func:`getItem`

        """
        itemID = None
        if name is None and title is None:
            raise AttributeError('Name or Title needs to be specified')
        for item in userContent:
            if title is None and name is not None:
                if item.name == name and (itemType is None or item.type == itemType):
                    return item.id

            elif title is not None and name is None:
                if item.title == title and (itemType is None or item.type == itemType):
                    return item.id

            else:
                if item.name == name and item.title == title and (itemType is None or item.type == itemType):
                    return item.id
        return None
    #----------------------------------------------------------------------    
    def getItem(self, userContent, title=None, name=None, itemType=None):
        """Gets an item by a combination of title, name, and type.
        
        Args:
            userContent (list): A list of user content.
            title (str): The title of the item. Defaults to ``None``.
            name (str): The name of the item. Defaults to ``None``.
            itemType (str): The type of the item. Defaults to ``None``.
        Returns:
            str: The item's ID. If the item does not exist, ``None``.        
        Raises:
            AttributeError: If both ``title`` and ``name`` are not specified (``None``).
        See Also:
            :py:func:`getItemID`

        """
        itemID = None
        if name is None and title is None:
            raise AttributeError('Name or Title needs to be specified')
        for item in userContent:
            if title is None and name is not None:
                if item.name == name and (itemType is None or item.type == itemType):
                    return item

            elif title is not None and name is None:
                if item.title == title and (itemType is None or item.type == itemType):
                    return item

            else:
                if item.name == name and item.title == title and (itemType is None or item.type == itemType):
                    return item
        return None
    #----------------------------------------------------------------------
    def folderExist(self, name, folders):
        """Determines if a folder exists, case insensitively.
        
        Args:
            name (str): The name of the folder to check.
            folders (list): A list of folder dicts to check against. The dicts must contain
                the key:value pair ``title``.
        Returns:
            bool: ``True`` if the folder exists in the list, ``False`` otherwise.
          
        """
        if name is not None and name != '':

            folderID = None

            for folder in folders:
                if folder['title'].lower() == name.lower():
                    return True

            del folders

            return folderID

        else:
            return False
    #----------------------------------------------------------------------
    def publishItems(self, items_info):
        """Publishes a list of items.
        
        Args:
            items_info (list): A list of JSON configuration items to publish.
        
        Returns:
            list: A list of results from :py:meth:`arcrest.manageorg._content.User.addItem`.
            
        """
        if self.securityhandler is None:
            print ("Security handler required")
            return
        itemInfo = None
        item_results = None
        item_info = None
        admin = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            item_results = []
            for item_info in items_info:
                if 'ReplaceTag' in item_info:

                    itemInfo = {"ReplaceTag":item_info['ReplaceTag'] }
                else:
                    itemInfo = {"ReplaceTag":"{FeatureService}" }

                itemInfo['ItemInfo']  = self._publishItems(config=item_info)

                if itemInfo['ItemInfo'] is not None and 'name' in itemInfo['ItemInfo']:
                    print ("%s created" % itemInfo['ItemInfo']['name'])
                    item_results.append(itemInfo)
                else:
                    print (str(itemInfo['ItemInfo']))

            return item_results

        except common.ArcRestHelperError as e:
            raise e
        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "publishItems",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
            })
        finally:
            itemInfo = None
            item_results = None
            item_info = None
            admin = None

            del itemInfo
            del item_results
            del item_info
            del admin

            gc.collect()
     #----------------------------------------------------------------------
    def _publishItems(self, config):
        name = None
        tags = None
        description = None
        extent = None
        admin = None
        adminusercontent = None
        itemData = None
        itemId = None
        datestring = None
        snippet = None
        everyone = None
        org = None
        groupNames = None
        folderName = None
        thumbnail = None
        itemType = None
        itemParams = None
        content = None
        userInfo = None
        userCommunity = None
        results = None
        folderName = None
        folderId = None
        res = None
        sea = None
        group_ids = None
        shareResults = None
        updateParams = None
        url = None
        resultItem = {}
        try:
            name = ''
            tags = ''
            description = ''
            extent = ''
            webmap_data = ''

            if 'Data' in config:
                itemData = config['Data']

            if 'Url' in config:
                url = config['Url']

            name = config['Title']

            if 'DateTimeFormat' in config:
                loc_df = config['DateTimeFormat']
            else:
                loc_df = dateTimeFormat

            datestring = datetime.datetime.now().strftime(loc_df)
            name = name.replace('{DATE}',datestring)
            name = name.replace('{Date}',datestring)

            description = config['Description']
            tags = config['Tags']
            snippet = config['Summary']
            everyone = config['ShareEveryone']
            org = config['ShareOrg']
            groupNames = config['Groups']  #Groups are by ID. Multiple groups comma separated
            folderName = config['Folder']
            thumbnail = config['Thumbnail']
            itemType = config['Type']
            typeKeywords = config['typeKeywords']
            skipIfExist = False
            if 'SkipIfExist' in config:
                skipIfExist = config['SkipIfExist']
                if str(skipIfExist).lower() == 'true':
                    skipIfExist = True


            itemParams = arcrest.manageorg.ItemParameter()
            itemParams.title = name
            itemParams.thumbnail = thumbnail
            itemParams.type = itemType
            itemParams.overwrite = True
            itemParams.snippet = snippet
            itemParams.description = description
            itemParams.extent = extent

            itemParams.tags = tags
            itemParams.typeKeywords = ",".join(typeKeywords)

            admin = arcrest.manageorg.Administration(securityHandler=self.securityhandler)

            content = admin.content
            userInfo = content.users.user()
            userCommunity = admin.community

            if folderName is not None and folderName != "":
                if self.folderExist(name=folderName,folders=userInfo.folders) is None:
                    res = userInfo.createFolder(name=folderName)
                userInfo.currentFolder = folderName
            if 'id' in userInfo.currentFolder:
                folderId = userInfo.currentFolder['id']

            sea = arcrest.find.search(securityHandler=self._securityHandler)
            items = sea.findItem(title=name, itemType=itemType,searchorg=False)

            if items['total'] >= 1:
                for res in items['results']:
                    if 'type' in res and res['type'] == itemType:
                        if 'name' in res and res['name'] == name:
                            itemId = res['id']
                            break
                        if 'title' in res and res['title'] == name:
                            itemId = res['id']
                            break
            if not itemId is None:

                item = content.getItem(itemId).userItem

                if skipIfExist == True:
                    resultItem['itemId'] = item.id
                    resultItem['url'] = item.item._curl + "/data"
                    resultItem['folderId'] = folderId
                    resultItem['name'] = name
                    return resultItem

                results = item.updateItem(itemParameters=itemParams,
                                          data=itemData,serviceUrl=url)
                if 'error' in results:
                    return results
                if item.ownerFolder != folderId:
                    if folderId is None:
                        folderId = "/"
                    moveRes = userInfo.moveItems(items=item.id,folder=folderId)

            else:
                try:
                    item = userInfo.addItem(itemParameters=itemParams,
                                            overwrite=True,
                                            url=url,
                                            relationshipType=None,
                                            originItemId=None,
                                            destinationItemId=None,
                                            serviceProxyParams=None,
                                            metadata=None,
                                            filePath=itemData)

                    #updateParams = arcrest.manageorg.ItemParameter()
                    #updateParams.title = name
                    #updateResults = item.updateItem(itemParameters=updateParams)
                except Exception as e:
                    print (e)
            if item is None:
                return "Item could not be added"

            group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
            shareResults = userInfo.shareItems(items=item.id,
                                               groups=','.join(group_ids),
                                               everyone=everyone,
                                               org=org)

            resultItem['itemId'] = item.id
            resultItem['url'] = item.item._curl + "/data"
            resultItem['folderId'] = folderId
            resultItem['name'] = name
            return resultItem

        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "_publishItems",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
            })

        finally:
            name = None
            tags = None
            description = None
            extent = None
            admin = None
            adminusercontent = None
            itemData = None
            datestring = None
            snippet = None
            everyone = None
            org = None
            groupNames = None
            itemId = None
            thumbnail = None
            itemType = None
            itemParams = None
            content = None
            userInfo = None
            userCommunity = None
            results = None
            folderName = None
            folderId = None
            res = None
            sea = None
            group_ids = None
            shareResults = None
            updateParams = None

            del name
            del tags
            del description
            del extent
            del admin
            del adminusercontent
            del itemData
            del datestring
            del snippet
            del everyone
            del org
            del groupNames
            del itemId
            del thumbnail
            del itemType
            del itemParams
            del content
            del userInfo
            del userCommunity
            del results
            del folderName
            del folderId
            del res
            del sea
            del group_ids
            del shareResults
            del updateParams

            gc.collect()
    #----------------------------------------------------------------------
    def publishMap(self, maps_info, fsInfo=None, itInfo=None):
        """Publishes a list of maps.
        
        Args:
            maps_info (list): A list of JSON configuration maps to publish.
        
        Returns:
            list: A list of results from :py:meth:`arcrest.manageorg._content.UserItem.updateItem`.
            
        """
        if self.securityhandler is None:
            print ("Security handler required")
            return
        itemInfo = None
        itemId = None
        map_results = None
        replaceInfo = None
        replaceItem = None
        map_info = None
        admin = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            map_results = []
            for map_info in maps_info:
                itemInfo = {}

                if 'ReplaceInfo' in map_info:
                    replaceInfo = map_info['ReplaceInfo']
                else:
                    replaceInfo = None


                if replaceInfo != None:

                    for replaceItem in replaceInfo:
                        if replaceItem['ReplaceType'] == 'Layer':

                            if fsInfo is not None:

                                for fs in fsInfo:
                                    if fs is not None and replaceItem['ReplaceString'] == fs['ReplaceTag']:
                                        replaceItem['ReplaceString'] = fs['FSInfo']['url']
                                        replaceItem['ItemID'] = fs['FSInfo']['itemId']
                                        replaceItem['ItemFolder'] = fs['FSInfo']['folderId']
                                        if 'convertCase' in fs['FSInfo']:
                                            replaceItem['convertCase'] = fs['FSInfo']['convertCase']
                                    elif 'ItemID' in replaceItem:
                                        if 'ItemFolder' in replaceItem == False:

                                            itemId = replaceItem['ItemID']
                                            itemInfo = admin.content.getItem(itemId=itemId)
                                            if itemInfo.owner:
                                                if itemInfo.owner == self._securityHandler.username and itemInfo.ownerFolder:
                                                    replaceItem['ItemFolder'] = itemInfo.ownerFolder
                                                else:
                                                    replaceItem['ItemFolder'] = None
                        elif replaceItem['ReplaceType'] == 'Global':

                            if itInfo is not None:

                                for itm in itInfo:
                                    if itm is not None:

                                        if replaceItem['ReplaceString'] == itm['ReplaceTag']:
                                            if 'ItemInfo' in itm:
                                                if 'url' in itm['ItemInfo']:
                                                    replaceItem['ReplaceString'] = itm['ItemInfo']['url']


                if 'ReplaceTag' in map_info:

                    itemInfo = {"ReplaceTag":map_info['ReplaceTag'] }
                else:
                    itemInfo = {"ReplaceTag":"{WebMap}" }

                itemInfo['MapInfo']  = self._publishMap(config=map_info,
                                                   replaceInfo=replaceInfo)
                map_results.append(itemInfo)
                print ("%s webmap created" % itemInfo['MapInfo']['Name'])
            return map_results

        except common.ArcRestHelperError as e:
            raise e
        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                 "function": "publishMap",
                 "line": line,
                 "filename":  filename,
                 "synerror": synerror,
            })
        finally:
            itemInfo = None
            itemId = None
            replaceInfo = None
            replaceItem = None
            map_info = None
            admin = None

            del itemInfo
            del itemId
            del replaceInfo
            del replaceItem
            del map_info
            del admin

            gc.collect()
    #----------------------------------------------------------------------
    def _publishMap(self, config, replaceInfo=None, operationalLayers=None, tableLayers=None):
        name = None
        tags = None
        description = None
        extent = None
        webmap_data = None
        itemJson = None
        update_service = None
        admin = None
        adminusercontent = None
        resultMap = None
        json_data = None
        replaceItem = None
        opLayers = None
        opLayer = None
        layers = None
        item = None
        response = None
        layerIdx = None
        updatedLayer = None
        updated = None
        text = None
        itemParams = None
        updateResults = None
        loc_df = None
        datestring = None
        snippet = None
        everyone = None
        org = None
        groupNames = None
        folderName = None
        thumbnail = None
        itemType = None
        typeKeywords = None
        userCommunity = None
        userContent = None
        folderId = None
        res = None
        folderContent = None
        itemId = None
        group_ids = None
        shareResults = None
        updateParams = None
        try:
            name = ''
            tags = ''
            description = ''
            extent = ''
            webmap_data = None

            mapJson = config['ItemJSON']
            if isinstance(mapJson,list):
                webmap_data = []
                for jsonItem in mapJson:
                    #if os.path.exists(jsonItem) == False:
                        #return {"Results":{"error": "%s does not exist" % jsonItem}}
                    #if webmap_data is None:
                        #try:
                            #with open(jsonItem) as webMapInfo:
                                #webmap_data = json.load(webMapInfo)
                        #except:
                            #raise ValueError("%s is not a valid JSON File" % jsonItem)
                    #else:
                    try:
                        with open(jsonItem) as webMapInfo:

                            webmap_data.append(json.load(webMapInfo))
                    except:
                        raise ValueError("%s is not a valid JSON File" % jsonItem)
                webmap_data = common.merge_dicts(webmap_data)


            else:
                if os.path.exists(mapJson) == False:
                    return {"Results":{"error": "%s does not exist" % mapJson}}
                try:
                    with open(mapJson) as webMapInfo:

                        webmap_data = json.load(webMapInfo)
                except:
                    raise ValueError("%s is not a valid JSON File" % mapJson)
            update_service = 'FALSE'

            resultMap = {'Layers':[],'Tables':[],'Results':{}}

            if webmap_data is not None:
                layersInfo= {}

                if operationalLayers:
                    webmap_data['operationalLayers'] = operationalLayers
                if tableLayers:
                    webmap_data['tables'] = tableLayers
                if replaceInfo:
                    for replaceItem in replaceInfo:
                        if replaceItem['ReplaceType'] == 'Global':
                            webmap_data = common.find_replace(webmap_data,replaceItem['SearchString'],replaceItem['ReplaceString'])
                        elif replaceItem['ReplaceType'] == 'Layer':
                            if 'tables' in webmap_data:
                                opLayers = webmap_data['tables']
                                for opLayer in opLayers:
                                    layerInfo= {}
                                    if replaceItem['SearchString'] in opLayer['url']:

                                        opLayer['url'] = opLayer['url'].replace(replaceItem['SearchString'],replaceItem['ReplaceString'])
                                        if 'ItemID' in replaceItem:
                                            opLayer['itemId'] = replaceItem['ItemID']
                                        else:
                                            opLayer['itemId'] = None
                                            #opLayer['itemId'] = get_guid()
                                        if 'convertCase' in replaceItem:
                                            if replaceItem['convertCase'] == 'lower':
                                                layerInfo = {}

                                                layerInfo['convertCase'] = replaceItem['convertCase']
                                                layerInfo['fields'] = []
                                                if 'layerDefinition' in opLayer:

                                                    if 'drawingInfo' in opLayer["layerDefinition"]:
                                                        if 'renderer' in opLayer["layerDefinition"]['drawingInfo']:
                                                            if 'field1' in opLayer["layerDefinition"]['drawingInfo']['renderer']:
                                                                opLayer["layerDefinition"]['drawingInfo']['renderer']['field1'] = opLayer["layerDefinition"]['drawingInfo']['renderer']['field1'].lower()
                                                        if 'labelingInfo' in opLayer["layerDefinition"]['drawingInfo']:

                                                            lblInfos = opLayer["layerDefinition"]['drawingInfo']['labelingInfo']
                                                            if len(lblInfos) > 0:
                                                                for lblInfo in lblInfos:
                                                                    if 'labelExpression' in lblInfo:
                                                                        result = re.findall(r"\[.*\]", lblInfo['labelExpression'])
                                                                        if len(result)>0:
                                                                            for res in result:
                                                                                lblInfo['labelExpression'] = str(lblInfo['labelExpression']).replace(res,str(res).lower())

                                                                    if 'labelExpressionInfo' in lblInfo:
                                                                        if 'value' in lblInfo['labelExpressionInfo']:

                                                                            result = re.findall(r"{.*}", lblInfo['labelExpressionInfo']['value'])
                                                                            if len(result)>0:
                                                                                for res in result:
                                                                                    lblInfo['labelExpressionInfo']['value'] = str(lblInfo['labelExpressionInfo']['value']).replace(res,str(res).lower())


                                                if 'popupInfo' in opLayer:

                                                    if 'mediaInfos' in opLayer['popupInfo'] and not opLayer['popupInfo']['mediaInfos'] is None:
                                                        for chart in opLayer['popupInfo']['mediaInfos']:
                                                            if 'value' in chart:
                                                                if 'normalizeField' in chart and not chart['normalizeField'] is None:
                                                                    chart['normalizeField'] = chart['normalizeField'].lower()
                                                                if 'fields' in chart['value']:

                                                                    for i in range(len(chart['value']['fields'])):
                                                                        chart['value']['fields'][i] = str(chart['value']['fields'][i]).lower()
                                                    if 'fieldInfos' in opLayer['popupInfo']:

                                                        for field in opLayer['popupInfo']['fieldInfos']:
                                                            newFld = str(field['fieldName']).lower()
                                                            if 'description' in opLayer['popupInfo']:
                                                                opLayer['popupInfo']['description'] = common.find_replace(obj = opLayer['popupInfo']['description'],
                                                                                                                          find = "{" + field['fieldName'] + "}",
                                                                                                                          replace = "{" + newFld + "}")


                                                            layerInfo['fields'].append({"PublishName":field['fieldName'],
                                                                                        'ConvertName':newFld})
                                                            field['fieldName'] = newFld
                                                layersInfo[opLayer['id']] = layerInfo

                            opLayers = webmap_data['operationalLayers']
                            for opLayer in opLayers:
                                layerInfo= {}
                                if replaceItem['SearchString'] in opLayer['url']:

                                    opLayer['url'] = opLayer['url'].replace(replaceItem['SearchString'],replaceItem['ReplaceString'])
                                    if 'ItemID' in replaceItem:
                                        opLayer['itemId'] = replaceItem['ItemID']
                                    else:
                                        opLayer['itemId'] = None
                                        #opLayer['itemId'] = get_guid()
                                    if 'convertCase' in replaceItem:
                                        if replaceItem['convertCase'] == 'lower':
                                            layerInfo = {}

                                            layerInfo['convertCase'] = replaceItem['convertCase']
                                            layerInfo['fields'] = []
                                            if 'layerDefinition' in opLayer:

                                                if 'drawingInfo' in opLayer["layerDefinition"]:
                                                    if 'renderer' in opLayer["layerDefinition"]['drawingInfo']:
                                                        if 'field1' in opLayer["layerDefinition"]['drawingInfo']['renderer']:
                                                            opLayer["layerDefinition"]['drawingInfo']['renderer']['field1'] = opLayer["layerDefinition"]['drawingInfo']['renderer']['field1'].lower()
                                                    if 'labelingInfo' in opLayer["layerDefinition"]['drawingInfo']:

                                                        lblInfos = opLayer["layerDefinition"]['drawingInfo']['labelingInfo']
                                                        if len(lblInfos) > 0:
                                                            for lblInfo in lblInfos:
                                                                if 'labelExpression' in lblInfo:
                                                                    result = re.findall(r"\[.*\]", lblInfo['labelExpression'])
                                                                    if len(result)>0:
                                                                        for res in result:
                                                                            lblInfo['labelExpression'] = str(lblInfo['labelExpression']).replace(res,str(res).lower())

                                                                if 'labelExpressionInfo' in lblInfo:
                                                                    if 'value' in lblInfo['labelExpressionInfo']:

                                                                        result = re.findall(r"{.*}", lblInfo['labelExpressionInfo']['value'])
                                                                        if len(result)>0:
                                                                            for res in result:
                                                                                lblInfo['labelExpressionInfo']['value'] = str(lblInfo['labelExpressionInfo']['value']).replace(res,str(res).lower())

                                            if 'popupInfo' in opLayer:

                                                if 'mediaInfos' in opLayer['popupInfo'] and not opLayer['popupInfo']['mediaInfos'] is None:
                                                    for k in range(len(opLayer['popupInfo']['mediaInfos'])):
                                                        chart = opLayer['popupInfo']['mediaInfos'][k]
                                                        if 'value' in chart:
                                                            if 'normalizeField' in chart and not chart['normalizeField'] is None:
                                                                chart['normalizeField'] = chart['normalizeField'].lower()
                                                            if 'fields' in chart['value']:

                                                                for i in range(len(chart['value']['fields'])):
                                                                    chart['value']['fields'][i] = str(chart['value']['fields'][i]).lower()
                                                            opLayer['popupInfo']['mediaInfos'][k] = chart
                                                if 'fieldInfos' in opLayer['popupInfo']:

                                                    for field in opLayer['popupInfo']['fieldInfos']:
                                                        newFld = str(field['fieldName']).lower()
                                                        if 'description' in opLayer['popupInfo']:
                                                            opLayer['popupInfo']['description'] = common.find_replace(obj = opLayer['popupInfo']['description'],
                                                                               find = "{" + field['fieldName'] + "}",
                                                                               replace = "{" + newFld + "}")


                                                        layerInfo['fields'].append({"PublishName":field['fieldName'],
                                                                                    'ConvertName':newFld})
                                                        field['fieldName'] = newFld
                                            layersInfo[opLayer['id']] = layerInfo


                opLayers = webmap_data['operationalLayers']
                resultMap['Layers'] = {}
                for opLayer in opLayers:
                    currentID = opLayer['id']

                    #if 'url' in opLayer:
                        #opLayer['id'] = common.getLayerName(url=opLayer['url']) + "_" + str(common.random_int_generator(maxrange = 9999))

                    if 'applicationProperties' in webmap_data:
                        if 'editing' in webmap_data['applicationProperties'] and \
                           not webmap_data['applicationProperties']['editing'] is None:
                            if 'locationTracking' in webmap_data['applicationProperties']['editing'] and \
                                not webmap_data['applicationProperties']['editing']['locationTracking'] is None:
                                if 'info' in webmap_data['applicationProperties']['editing']['locationTracking'] and \
                                   not webmap_data['applicationProperties']['editing']['locationTracking']['info'] is None:
                                    if 'layerId' in webmap_data['applicationProperties']['editing']['locationTracking']['info']:
                                        if webmap_data['applicationProperties']['editing']['locationTracking']['info']['layerId'] == currentID:
                                            webmap_data['applicationProperties']['editing']['locationTracking']['info']['layerId'] = opLayer['id']
                        if 'viewing' in webmap_data['applicationProperties'] and \
                           not webmap_data['applicationProperties']['viewing'] is None:
                            if 'search' in webmap_data['applicationProperties']['viewing'] and \
                                not webmap_data['applicationProperties']['viewing']['search'] is None:
                                if 'layers' in webmap_data['applicationProperties']['viewing']['search'] and \
                                    not webmap_data['applicationProperties']['viewing']['search']['layers'] is None:

                                    for k in range(len(webmap_data['applicationProperties']['viewing']['search']['layers'])):
                                        searchlayer =  webmap_data['applicationProperties']['viewing']['search']['layers'][k]
                                        if searchlayer['id'] == currentID:
                                            searchlayer['id'] = opLayer['id']
                                            if 'fields' in searchlayer and \
                                               not searchlayer['fields'] is None:
                                                for i in range(len(searchlayer['fields'])):

                                                    searchlayer['fields'][i]['Name'] = str(searchlayer['fields'][i]['Name']).lower()
                                            if 'field' in searchlayer and \
                                               not searchlayer['field'] is None:
                                                searchlayer['field']['name'] = searchlayer['field']['name'].lower()

                                            webmap_data['applicationProperties']['viewing']['search']['layers'][k] = searchlayer

                    if 'applicationProperties' in webmap_data:
                        webmap_data['applicationProperties'] = common.find_replace(webmap_data['applicationProperties'], currentID, opLayer['id'])

                    resultLayer = {"Name":opLayer['title'],
                                  "ID":opLayer['id']
                                  }

                    if currentID in layersInfo:
                        resultLayer['FieldInfo'] = layersInfo[currentID]
                    resultMap['Layers'][currentID] = resultLayer


                if 'tables' in webmap_data:

                    opLayers = webmap_data['tables']
                    for opLayer in opLayers:
                        currentID = opLayer['id']

                        #opLayer['id'] = common.getLayerName(url=opLayer['url']) + "_" + str(common.random_int_generator(maxrange = 9999))
                        if 'applicationProperties' in webmap_data:
                            if 'editing' in webmap_data['applicationProperties'] and \
                               not webmap_data['applicationProperties']['editing'] is None:
                                if 'locationTracking' in webmap_data['applicationProperties']['editing'] and \
                                   not webmap_data['applicationProperties']['editing']['locationTracking'] is None:
                                    if 'info' in webmap_data['applicationProperties']['editing']['locationTracking'] and \
                                       not webmap_data['applicationProperties']['editing']['locationTracking']['info'] is None:
                                        if 'layerId' in webmap_data['applicationProperties']['editing']['locationTracking']['info']:
                                            if webmap_data['applicationProperties']['editing']['locationTracking']['info']['layerId'] == currentID:
                                                webmap_data['applicationProperties']['editing']['locationTracking']['info']['layerId'] = opLayer['id']
                            if 'viewing' in webmap_data['applicationProperties'] and \
                               not webmap_data['applicationProperties']['viewing'] is None:
                                if 'search' in webmap_data['applicationProperties']['viewing'] and \
                                   not webmap_data['applicationProperties']['viewing']['search'] is None:
                                    if 'layers' in webmap_data['applicationProperties']['viewing']['search'] and \
                                       not webmap_data['applicationProperties']['viewing']['search']['layers'] is None:

                                        for k in range(len(webmap_data['applicationProperties']['viewing']['search']['layers'])):
                                            searchlayer =  webmap_data['applicationProperties']['viewing']['search']['layers'][k]
                                            if searchlayer['id'] == currentID:
                                                searchlayer['id'] = opLayer['id']
                                                if 'fields' in searchlayer and \
                                                   not searchlayer['fields'] is None:
                                                    for i in range(len(searchlayer['fields'])):

                                                        searchlayer['fields'][i]['Name'] = str(searchlayer['fields'][i]['Name']).lower()
                                                if 'field' in searchlayer and \
                                                   not searchlayer['field'] is None:
                                                    searchlayer['field']['name'] = searchlayer['field']['name'].lower()

                                                webmap_data['applicationProperties']['viewing']['search']['layers'][k] = searchlayer

                        if 'applicationProperties' in webmap_data:
                            webmap_data['applicationProperties'] = common.find_replace(webmap_data['applicationProperties'], currentID, opLayer['id'])

                        resultMap['Tables'].append({"Name":opLayer['title'],"ID":opLayer['id']})


            name = config['Title']

            if 'DateTimeFormat' in config:
                loc_df = config['DateTimeFormat']
            else:
                loc_df = dateTimeFormat

            datestring = datetime.datetime.now().strftime(loc_df)
            name = name.replace('{DATE}',datestring)
            name = name.replace('{Date}',datestring)

            description = config['Description']
            tags = config['Tags']
            snippet = config['Summary']

            extent = config['Extent']

            everyone = config['ShareEveryone']
            org = config['ShareOrg']
            groupNames = config['Groups']  #Groups are by ID. Multiple groups comma separated

            folderName = config['Folder']
            thumbnail = config['Thumbnail']

            itemType = config['Type']
            typeKeywords = config['typeKeywords']

            if webmap_data is None:
                return None

            itemParams = arcrest.manageorg.ItemParameter()
            itemParams.title = name
            itemParams.thumbnail = thumbnail
            itemParams.type = "Web Map"
            itemParams.overwrite = True
            itemParams.snippet = snippet
            itemParams.description = description
            itemParams.extent = extent

            itemParams.tags = tags
            itemParams.typeKeywords = ",".join(typeKeywords)

            admin = arcrest.manageorg.Administration(securityHandler=self.securityhandler)

            content = admin.content
            userInfo = content.users.user()
            userCommunity = admin.community

            if folderName is not None and folderName != "":
                if self.folderExist(name=folderName,folders=userInfo.folders) is None:
                    res = userInfo.createFolder(name=folderName)
                userInfo.currentFolder = folderName
            if 'id' in userInfo.currentFolder:
                folderId = userInfo.currentFolder['id']


            sea = arcrest.find.search(securityHandler=self._securityHandler)
            items = sea.findItem(title=name, itemType=itemType,searchorg=False)

            if items['total'] >= 1:
                for res in items['results']:
                    if 'type' in res and res['type'] == itemType:
                        if 'name' in res and res['name'] == name:
                            itemId = res['id']
                            break
                        if 'title' in res and res['title'] == name:
                            itemId = res['id']
                            break
            if not itemId is None:
                item = content.getItem(itemId).userItem
                results = item.updateItem(itemParameters=itemParams,
                                            text=json.dumps(webmap_data))
                if 'error' in results:
                    return results
                if item.ownerFolder != folderId:
                    if folderId is None:
                        folderId = "/"
                    moveRes = userInfo.moveItems(items=item.id,folder=folderId)
            else:
                try:
                    item = userInfo.addItem(itemParameters=itemParams,
                            overwrite=True,
                            url=None,
                            relationshipType=None,
                            originItemId=None,
                            destinationItemId=None,
                            serviceProxyParams=None,
                            metadata=None,
                            text=json.dumps(webmap_data))

                except Exception as e:
                    print (e)
            if item is None:
                return "Item could not be added"

            group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
            shareResults = userInfo.shareItems(items=item.id,
                                               groups=','.join(group_ids),
                                               everyone=everyone,
                                               org=org)
            updateParams = arcrest.manageorg.ItemParameter()
            updateParams.title = name
            updateResults = item.updateItem(itemParameters=updateParams)

            resultMap['Results']['itemId'] = item.id
            resultMap['folderId'] = folderId
            resultMap['Name'] = name
            return resultMap


        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "_publishMap",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
            })

        finally:
            name = None
            tags = None
            description = None
            extent = None
            webmap_data = None
            itemJson = None
            update_service = None
            admin = None
            adminusercontent = None
            resultMap = None
            json_data = None
            replaceItem = None
            opLayers = None
            opLayer = None
            layers = None
            item = None
            response = None
            layerIdx = None
            updatedLayer = None
            updated = None
            text = None
            itemParams = None
            updateResults = None
            loc_df = None
            datestring = None
            snippet = None
            everyone = None
            org = None
            groupNames = None
            folderName = None
            thumbnail = None
            itemType = None
            typeKeywords = None
            userCommunity = None
            userContent = None
            folderId = None
            res = None
            folderContent = None
            itemId = None
            group_ids = None
            shareResults = None
            updateParams = None

            del name
            del tags
            del description
            del extent
            del webmap_data
            del itemJson
            del update_service
            del admin
            del adminusercontent
            del resultMap
            del json_data
            del replaceItem
            del opLayers
            del opLayer
            del layers
            del item
            del response
            del layerIdx
            del updatedLayer
            del updated
            del text
            del itemParams
            del updateResults
            del loc_df
            del datestring
            del snippet
            del everyone
            del org
            del groupNames
            del folderName
            del thumbnail
            del itemType
            del typeKeywords
            del userCommunity
            del userContent
            del folderId
            del res
            del folderContent
            del itemId
            del group_ids
            del shareResults
            del updateParams

            gc.collect()
    #----------------------------------------------------------------------
    def publishCombinedWebMap(self, maps_info, webmaps):
        """Publishes a combination of web maps.
        
        Args:
            maps_info (list): A list of JSON configuration combined web maps to publish.
        
        Returns:
            list: A list of results from :py:meth:`arcrest.manageorg._content.UserItem.updateItem`.
            
        """
        if self.securityhandler is None:
            print ("Security handler required")
            return
        admin = None
        map_results = None
        map_info = None
        operationalLayers = None
        tableLayers = None
        item = None
        response = None
        opLays = None
        operationalLayers = None
        tblLays = None
        tblLayer = None
        itemInfo = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)

            map_results = []
            for map_info in maps_info:

                operationalLayers = []
                tableLayers = []
                for webmap in webmaps:
                    item = admin.content.getItem(itemId=webmap)
                    response = item.itemData()
                    if 'operationalLayers' in response:

                        opLays = []
                        for opLayer in response['operationalLayers']:
                            opLays.append(opLayer)
                        opLays.extend(operationalLayers)
                        operationalLayers = opLays
                    if 'tables' in response:

                        tblLays = []
                        for tblLayer in response['tables']:
                            tblLays.append(tblLayer)
                        tblLays.extend(tableLayers)
                        tableLayers = tblLays

                if 'ReplaceTag' in map_info:

                    itemInfo = {"ReplaceTag":map_info['ReplaceTag'] }
                else:
                    itemInfo = {"ReplaceTag":"{WebMap}" }

                itemInfo['MapInfo'] = self._publishMap(config=map_info,
                                                        replaceInfo=None,
                                                        operationalLayers=operationalLayers,
                                                        tableLayers=tableLayers)


                map_results.append(itemInfo)
                if not itemInfo is None:
                    if not 'error' in itemInfo['MapInfo']['Results']:
                        print ("%s webmap created" % itemInfo['MapInfo']['Name'])
                    else:
                        print (str(itemInfo['MapInfo']['Results']))
                else:
                    print ("Map not created")

                return map_results
        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "publishedCombinedWebMap",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
            })
        finally:
            admin = None

            map_info = None

            tableLayers = None
            item = None
            response = None
            opLays = None
            operationalLayers = None
            tblLays = None
            tblLayer = None
            itemInfo = None

            del admin
            del map_info

            del tableLayers
            del item
            del response
            del opLays
            del operationalLayers
            del tblLays
            del tblLayer
            del itemInfo

            gc.collect()
    #----------------------------------------------------------------------
    def publishFsFromMXD(self, fs_config):
        """Publishes the layers in a MXD to a feauture service.
        
        Args:
            fs_config (list): A list of JSON configuration feature service details to publish.
        Returns:
            dict: A dictionary of results objects.

        """
        fs = None
        res = None
        resItm = None
        if self.securityhandler is None:
            print ("Security handler required")
            return
        if self.securityhandler.is_portal:
            url = self.securityhandler.org_url
        else:
            url = 'http://www.arcgis.com'
        try:
            res = []
            if isinstance(fs_config, list):
                for fs in fs_config:
                    if 'ReplaceTag' in fs:

                        resItm = {"ReplaceTag":fs['ReplaceTag'] }
                    else:
                        resItm = {"ReplaceTag":"{FeatureService}" }

                    resItm['FSInfo'] = self._publishFSFromMXD(config=fs, url=url)

                    if not resItm['FSInfo'] is None and 'url' in resItm['FSInfo']:
                        print ("%s created" % resItm['FSInfo']['url'])
                        res.append(resItm)
                    else:
                        print (str(resItm['FSInfo']))

            else:
                if 'ReplaceTag' in fs_config:

                    resItm = {"ReplaceTag":fs_config['ReplaceTag'] }
                else:
                    resItm = {"ReplaceTag":"{FeatureService}" }

                resItm['FSInfo'] = self._publishFSFromMXD(config=fs_config, url=url)

                if 'url' in resItm['FSInfo']:
                    print ("%s created" % resItm['FSInfo']['url'])
                    res.append(resItm)
                else:
                    print (str(resItm['FSInfo']))

            return res
        except common.ArcRestHelperError as e:
            raise e
        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                        "function": "publishFsFromMXD",
                        "line": line,
                        "filename":  filename,
                        "synerror": synerror,
                                        }
                                        )

        finally:
            resItm = None
            fs = None

            del resItm
            del fs

            gc.collect()
    #----------------------------------------------------------------------
    def publishFeatureCollections(self, configs):
        """Publishes feature collections to a feature service.
        
        Args:
            configs (list): A list of JSON configuration feature service details to publish.
        Returns:
            dict: A dictionary of results objects.

        """
        if self.securityhandler is None:
            print ("Security handler required")
            return
        config = None
        res = None
        resItm = None
        try:
            res = []
            if isinstance(configs, list):
                for config in configs:
                    if 'ReplaceTag' in config:

                        resItm = {"ReplaceTag":config['ReplaceTag'] }
                    else:
                        resItm = {"ReplaceTag":"{FeatureService}" }

                    if 'Zip' in config:
                        resItm['FCInfo'] = self._publishFeatureCollection(config=config)


                    if not resItm['FCInfo'] is None and 'id' in resItm['FCInfo']:
                        print ("%s feature collection created" % resItm['FCInfo']['id'])
                        res.append(resItm)
                    else:
                        print (str(resItm['FCInfo']))


            return res

        except common.ArcRestHelperError as e:
            raise e
        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "publishFeatureCollections",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
            })

        finally:
            resItm = None
            config = None

            del resItm
            del config

            gc.collect()
    #----------------------------------------------------------------------
    def _publishFSFromMXD(self, config, url='http://www.arcgis.com'):
        mxd = None
        q = None
        everyone = None
        org = None
        groupNames = None

        folderName = None
        thumbnail = None
        capabilities = None
        maxRecordCount = None
        loc_df = None
        datestring = None
        service_name = None
        service_name_safe = None
        sd_Info = None
        admin = None
        itemParams = None
        adminusercontent = None
        userCommunity = None
        userContent = None
        folderId = None
        res = None
        folderContent = None
        itemId = None
        resultSD = None
        publishParameters = None
        resultFS = None
        delres = None
        status = None
        group_ids = None
        shareResults = None
        updateParams = None
        enableEditTracking = None
        adminFS = None
        json_dict = None
        enableResults = None
        layer = None
        layers = None
        layUpdateResult = None
        definition = None
        try:
            # Report settings
            dataFile = None
            if 'Mxd' in config:
                dataFile = config['Mxd']
            elif 'Zip' in config:
                dataFile = config['Zip']
            # Service settings
            service_name = config['Title']

            everyone = config['ShareEveryone']
            org = config['ShareOrg']
            groupNames = config['Groups']  #Groups are by ID. Multiple groups comma separated
            if 'EnableEditTracking' in config:
                print ("enableEditTracking parameter has been deprecated, please add a definition section to the config")
                enableEditTracking = config['EnableEditTracking']
            else:
                #print ("Please add an EnableEditTracking parameter to your feature service section")
                enableEditTracking = False
            folderName = config['Folder']
            thumbnail = config['Thumbnail']

            if 'Capabilities' in config:
                print ("Capabilities parameter has been deprecated, please add a definition section to the config")

                capabilities = config['Capabilities']
            if 'Definition' in config:
                definition = config['Definition']

                if 'capabilities' in definition:
                    capabilities = definition['capabilities']
            if 'maxRecordCount' in config:
                maxRecordCount =  config["maxRecordCount"]
            else:
                maxRecordCount = '1000' # If not cast as a string, the MXDtoFeatureServiceDef method called below returns an error stating 'cannot serialize 1000 (type int)'

            if 'DateTimeFormat' in config:
                loc_df = config['DateTimeFormat']
            else:
                loc_df = dateTimeFormat
            skipIfExist = False
            if 'SkipIfExist' in config:
                skipIfExist = config['SkipIfExist']
                if str(skipIfExist).lower() == 'true':
                    skipIfExist = True


            datestring = datetime.datetime.now().strftime(loc_df)
            service_name = service_name.replace('{DATE}',datestring)
            service_name = service_name.replace('{Date}',datestring)

            service_name_safe = service_name.replace(' ','_')
            service_name_safe = service_name_safe.replace(':','_')
            service_name_safe = service_name_safe.replace('-','_')

            if os.path.exists(path=dataFile) == False:
                raise ValueError("data file does not exit")

            extension = os.path.splitext(dataFile)[1]


            admin = arcrest.manageorg.Administration(securityHandler=self.securityhandler)
            hostingServers = admin.hostingServers
            if len(hostingServers) == 0:
                return ("No hosting servers can be found, if this is portal, update the settings to include a hosting server.")

            content = admin.content
            userInfo = content.users.user()
            userCommunity = admin.community

            if folderName is not None and folderName != "":
                if self.folderExist(name=folderName,folders=userInfo.folders) is None:
                    res = userInfo.createFolder(name=folderName)
                userInfo.currentFolder = folderName
            if 'id' in userInfo.currentFolder:
                folderId = userInfo.currentFolder['id']

            if skipIfExist == True:
                sea = arcrest.find.search(securityHandler=self._securityHandler)
                items = sea.findItem(title=service_name, itemType='Feature Service',searchorg=False)
                if 'total' in items:
                    if items['total'] >= 1:
                        for res in items['results']:
                            if 'type' in res and res['type'] == 'Feature Service':
                                if 'name' in res and res['name'] == service_name:
                                    itemId = res['id']
                                    break
                                if 'title' in res and res['title'] == service_name:
                                    itemId = res['id']
                                    break
                        if itemId is not None:
                            defItem = content.getItem(itemId)

                            results = {
                                "url": defItem.url,
                                "folderId": folderId,
                                "itemId": defItem.id,
                                "convertCase": self._featureServiceFieldCase,
                                "messages":"Exist"
                            }
                            return results
                else:
                    print ("Error searching organzation, {0}".format(items))

            if (extension == ".mxd"):
                dataFileType = "serviceDefinition"
                searchType = "Service Definition"
                sd_Info = arcrest.common.servicedef.MXDtoFeatureServiceDef(mxd_path=dataFile,
                                                                     service_name=service_name_safe,
                                                                     tags=None,
                                                                     description=None,
                                                                     folder_name=None,
                                                                     capabilities=capabilities,
                                                                     maxRecordCount=maxRecordCount,
                                                                     server_type='MY_HOSTED_SERVICES',
                                                                     url=url)
                if sd_Info is not None:
                    publishParameters = arcrest.manageorg.PublishSDParameters(tags=sd_Info['tags'],
                                                                              overwrite='true')
            elif (extension == ".zip"):
                dataFileType = "Shapefile"
                searchType = "Shapefile"
                sd_Info = {'servicedef':dataFile,'tags':config['Tags']}
                description = ""
                if 'Description' in config:
                    description = config['Description']
                publishParameters = arcrest.manageorg.PublishShapefileParameter(name=service_name,
                                                                            layerInfo={'capabilities':capabilities},
                                                                            description=description)
                if 'hasStaticData' in definition:
                    publishParameters.hasStaticData = definition['hasStaticData']

            if sd_Info is None:
                print ("Publishing SD or Zip not valid")
                raise common.ArcRestHelperError({
                    "function": "_publishFsFromMXD",
                    "line": lineno(),
                    "filename":  'publishingtools.py',
                    "synerror": "Publishing SD or Zip not valid"
                })


            itemParams = arcrest.manageorg.ItemParameter()
            #if isinstance(hostingServers[0],arcrest.manageags.administration.AGSAdministration):
                #itemParams.title = service_name_safe
            #else:
                #itemParams.title = service_name
            itemParams.title = service_name
            itemParams.thumbnail = thumbnail
            itemParams.type = searchType
            itemParams.overwrite = True

            sea = arcrest.find.search(securityHandler=self._securityHandler)
            items = sea.findItem(title=service_name, itemType=searchType,searchorg=False)
            defItem = None
            defItemID = None
            if items['total'] >= 1:
                for res in items['results']:
                    if 'type' in res and res['type'] == searchType:
                        if 'name' in res and res['name'] == service_name:
                            defItemID = res['id']
                            break
                        if 'title' in res and res['title'] == service_name:
                            defItemID = res['id']
                            break
                #itemId = items['results'][0]['id']



            if not defItemID is None:
                defItem = content.getItem(defItemID).userItem

                resultSD = defItem.updateItem(itemParameters=itemParams,
                                            data=sd_Info['servicedef'])
                if 'error' in resultSD:
                    return resultSD
                if defItem.ownerFolder != folderId:
                    if folderId is None:
                        folderId = "/"
                    moveRes = userInfo.moveItems(items=defItem.id,folder=folderId)

            else:
                try:
                    defItem = userInfo.addItem(itemParameters=itemParams,
                            filePath=sd_Info['servicedef'],
                            overwrite=True,
                            url=None,
                            text=None,
                            relationshipType=None,
                            originItemId=None,
                            destinationItemId=None,
                            serviceProxyParams=None,
                            metadata=None)
                except Exception as e:
                    print (e)
                if defItem is None:
                    return "Item could not be added "


            try:
                serviceItem = userInfo.publishItem(
                    fileType=dataFileType,
                    itemId=defItem.id,
                    publishParameters=publishParameters,
                    overwrite = True,
                    wait=True)
            except Exception as e:
                print ("Error publishing item: Error Details: {0}".format(str(e)))

                sea = arcrest.find.search(securityHandler=self._securityHandler)
                items = sea.findItem(title =service_name, itemType='Feature Service',searchorg=False)

                if items['total'] >= 1:
                    for res in items['results']:
                        if 'type' in res and res['type'] == 'Feature Service':
                            if 'name' in res and res['name'] == service_name:
                                itemId = res['id']
                                break
                            if 'title' in res and res['title'] == service_name:
                                itemId = res['id']
                                break
                if not itemId is None:

                    sea = arcrest.find.search(securityHandler=self._securityHandler)
                    items = sea.findItem(title =service_name_safe, itemType='Feature Service',searchorg=False)

                    if items['total'] >= 1:
                        for res in items['results']:
                            if 'type' in res and res['type'] == 'Feature Service':
                                if 'name' in res and res['name'] == service_name_safe:
                                    itemId = res['id']
                                    break
                                if 'title' in res and res['title'] == service_name_safe:
                                    itemId = res['id']
                                    break
                if not itemId is None:
                    existingItem = admin.content.getItem(itemId = itemId).userItem
                    if existingItem.url is not None:
                        adminFS = AdminFeatureService(url=existingItem.url, securityHandler=self._securityHandler)
                        cap = str(adminFS.capabilities)
                        existingDef = {}

                        if 'Sync' in cap:
                            print ("Disabling Sync")
                            capItems = cap.split(',')
                            if 'Sync' in capItems:
                                capItems.remove('Sync')

                            existingDef['capabilities'] = ','.join(capItems)
                            enableResults = adminFS.updateDefinition(json_dict=existingDef)

                            if 'error' in enableResults:
                                delres = userInfo.deleteItems(items=existingItem.id)
                                if 'error' in delres:
                                    print (delres)
                                    return delres
                                print ("Delete successful")
                            else:
                                print ("Sync Disabled")
                        else:
                            print ("Attempting to delete")
                            delres = userInfo.deleteItems(items=existingItem.id)
                            if 'error' in delres:
                                print (delres)
                                return delres
                            print ("Delete successful")
                        adminFS = None
                        del adminFS
                    else:
                        print ("Attempting to delete")
                        delres = userInfo.deleteItems(items=existingItem.id)
                        if 'error' in delres:
                            print (delres)
                            return delres
                        print ("Delete successful")
                else:
                    print ("Item exist and cannot be found, probably owned by another user.")
                    raise common.ArcRestHelperError({
                        "function": "_publishFsFromMXD",
                        "line": lineno(),
                        "filename":  'publishingtools.py',
                        "synerror": "Item exist and cannot be found, probably owned by another user."
                    }
                    )

                try:
                    serviceItem = userInfo.publishItem(
                        fileType=dataFileType,
                        itemId=defItem.id,
                        overwrite = True,
                        publishParameters=publishParameters,
                        wait=True)
                except Exception as e:

                    print ("Overwrite failed, deleting")
                    delres = userInfo.deleteItems(items=existingItem.id)
                    if 'error' in delres:
                        print (delres)
                        return delres

                    print ("Delete successful")
                    try:
                        serviceItem = userInfo.publishItem(
                            fileType=dataFileType,
                            itemId=defItem.id,
                            overwrite = True,
                            publishParameters=publishParameters,
                            wait=True)
                    except Exception as e:
                        return e

            results = {
                "url": serviceItem.url,
                "folderId": folderId,
                "itemId": serviceItem.id,
                "convertCase": self._featureServiceFieldCase,
                "messages":""
            }
            group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
            shareResults = userInfo.shareItems(items=serviceItem.id,
                                    groups=','.join(group_ids),
                                    everyone=everyone,
                                    org=org)
            updateParams = arcrest.manageorg.ItemParameter()
            updateParams.title = service_name
            updateResults = serviceItem.updateItem(itemParameters=updateParams)
            adminFS = AdminFeatureService(url=serviceItem.url, securityHandler=self._securityHandler)

            if enableEditTracking == True or str(enableEditTracking).upper() == 'TRUE':

                json_dict = {'editorTrackingInfo':{}}
                json_dict['editorTrackingInfo']['allowOthersToDelete'] = True
                json_dict['editorTrackingInfo']['allowOthersToUpdate'] = True
                json_dict['editorTrackingInfo']['enableEditorTracking'] = True
                json_dict['editorTrackingInfo']['enableOwnershipAccessControl'] = False

                enableResults = adminFS.updateDefinition(json_dict=json_dict)
                if 'error' in enableResults:
                    results['messages'] += enableResults

                json_dict = {'editFieldsInfo':{}}

                json_dict['editFieldsInfo']['creationDateField'] = ""
                json_dict['editFieldsInfo']['creatorField'] = ""
                json_dict['editFieldsInfo']['editDateField'] = ""
                json_dict['editFieldsInfo']['editorField'] = ""

                layers = adminFS.layers
                tables = adminFS.tables
                for layer in layers:
                    if layer.canModifyLayer is None or layer.canModifyLayer == True:
                        if layer.editFieldsInfo is None:
                            layUpdateResult = layer.addToDefinition(json_dict=json_dict)
                            if 'error' in layUpdateResult:

                                layUpdateResult['error']['layerid'] = layer.id
                                results['messages'] += layUpdateResult['error']
                if not tables is None:
                    for layer in tables:
                        if layer.canModifyLayer is None or layer.canModifyLayer == True:
                            if layer.editFieldsInfo is None:
                                layUpdateResult = layer.addToDefinition(json_dict=json_dict)
                                if 'error' in layUpdateResult:

                                    layUpdateResult['error']['layerid'] = layer.id
                                    results['messages'] += layUpdateResult['error']


            if definition is not None:

                enableResults = adminFS.updateDefinition(json_dict=definition)
                if enableResults is not None and 'error' in enableResults:
                    results['messages'] = enableResults
                else:
                    if 'editorTrackingInfo' in definition:
                        if 'enableEditorTracking' in definition['editorTrackingInfo']:
                            if definition['editorTrackingInfo']['enableEditorTracking'] == True:

                                json_dict = {'editFieldsInfo':{}}

                                json_dict['editFieldsInfo']['creationDateField'] = ""
                                json_dict['editFieldsInfo']['creatorField'] = ""
                                json_dict['editFieldsInfo']['editDateField'] = ""
                                json_dict['editFieldsInfo']['editorField'] = ""

                                layers = adminFS.layers
                                tables = adminFS.tables
                                for layer in layers:
                                    if layer.canModifyLayer is None or layer.canModifyLayer == True:
                                        if layer.editFieldsInfo is None:
                                            layUpdateResult = layer.addToDefinition(json_dict=json_dict)
                                            if 'error' in layUpdateResult:

                                                layUpdateResult['error']['layerid'] = layer.id
                                                results['messages'] = layUpdateResult['error']
                                if not tables is None:
                                    for layer in tables:
                                        if layer.canModifyLayer is None or layer.canModifyLayer == True:
                                            if layer.editFieldsInfo is None:
                                                layUpdateResult = layer.addToDefinition(json_dict=json_dict)
                                                if 'error' in layUpdateResult:

                                                    layUpdateResult['error']['layerid'] = layer.id
                                                    results['messages'] = layUpdateResult['error']

            return results
        except common.ArcRestHelperError as e:
            raise e
        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "_publishFsFromMXD",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
            })
        finally:
            definition = None
            mxd = None
            q = None
            everyone = None
            org = None
            groupNames = None

            folderName = None
            thumbnail = None
            capabilities = None
            maxRecordCount = None
            loc_df = None
            datestring = None
            service_name = None
            service_name_safe = None
            sd_Info = None
            admin = None
            itemParams = None

            userCommunity = None
            userContent = None
            folderId = None
            res = None
            folderContent = None
            itemId = None
            resultSD = None
            publishParameters = None
            resultFS = None
            delres = None
            status = None
            group_ids = None
            shareResults = None
            updateParams = None
            enableEditTracking = None
            adminFS = None
            json_dict = None
            enableResults = None
            layer = None
            layers = None
            layUpdateResult = None

            del definition
            del layer
            del layers
            del layUpdateResult
            del mxd

            del q
            del everyone
            del org
            del groupNames

            del folderName
            del thumbnail
            del capabilities
            del maxRecordCount
            del loc_df
            del datestring
            del service_name
            del service_name_safe
            del sd_Info
            del admin
            del itemParams

            del userCommunity
            del userContent
            del folderId
            del res
            del folderContent
            del itemId
            del resultSD
            del publishParameters
            del resultFS
            del delres
            del status
            del group_ids
            del shareResults
            del updateParams
            del enableEditTracking
            del adminFS
            del json_dict
            del enableResults
            gc.collect()
    #----------------------------------------------------------------------
    def _publishAppLogic(self, appDet, map_info=None, fsInfo=None):
        itemInfo = None
        replaceInfo = None
        replaceItem = None
        mapDet = None
        lay = None
        itemId = None
        admin = None
        try:
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            itemInfo = {}

            if 'ReplaceInfo' in appDet:
                replaceInfo = appDet['ReplaceInfo']
            else:
                replaceInfo = None

            if replaceInfo != None:

                for replaceItem in replaceInfo:
                    if fsInfo is not None:
                        for fsDet in fsInfo:
                            if 'ReplaceTag' in fsDet:
                                if 'ReplaceString' in replaceItem:
                                    if fsDet is not None and replaceItem['ReplaceString'] == fsDet['ReplaceTag'] and \
                                       (replaceItem['ReplaceType'] == 'Service' or replaceItem['ReplaceType'] == 'Layer'):
                                        replaceItem['ReplaceString'] = fsDet['FSInfo']['url']
                                        replaceItem['ItemID'] = fsDet['FSInfo']['itemId']
                                        replaceItem['ItemFolder'] = fsDet['FSInfo']['folderId']
                                        if 'convertCase' in fsDet['FSInfo']:
                                            replaceItem['convertCase'] = fsDet['FSInfo']['convertCase']
                                        replaceItem['ReplaceType'] = "Global"
                    if map_info is not None:
                        for mapDet in map_info:
                            if 'ReplaceTag' in mapDet:
                                if 'ReplaceString' in replaceItem:
                                    if mapDet is not None and replaceItem['ReplaceString'] == mapDet['ReplaceTag'] and \
                                       replaceItem['ReplaceType'] == 'Map':

                                        replaceItem['ItemID'] = mapDet['MapInfo']['Results']['itemId']
                                        replaceItem['ItemFolder'] = mapDet['MapInfo']['folderId']
                                        replaceItem['LayerInfo'] = mapDet['MapInfo']['Layers']
                                    elif mapDet is not None and replaceItem['ReplaceType'] == 'Layer':
                                        repInfo = replaceItem['ReplaceString'].split("|")
                                        if len(repInfo) == 2:
                                            if repInfo[0] == mapDet['ReplaceTag']:
                                                for key,value in mapDet['MapInfo']['Layers'].items():
                                                    if value["Name"] == repInfo[1]:
                                                        replaceItem['ReplaceString'] = value["ID"]

                                if 'ItemID' in replaceItem:
                                    if 'ItemFolder' in replaceItem == False:

                                        itemId = replaceItem['ItemID']

                                        itemInfo = admin.content.getItem(itemId=itemId)

                                        if itemInfo.owner == self._securityHandler.username and itemInfo.ownerFolder:
                                            replaceItem['ItemFolder'] = itemInfo['ownerFolder']
                                        else:
                                            replaceItem['ItemFolder'] = None


            if 'ReplaceTag' in appDet:

                itemInfo = {"ReplaceTag":appDet['ReplaceTag'] }
            else:
                itemInfo = {"ReplaceTag":"{App}" }

            if appDet['Type'] == 'Web Mapping Application':
                itemInfo['AppInfo']  = self._publishApp(config=appDet,
                                                               replaceInfo=replaceInfo)
            elif appDet['Type'] == 'Operation View':
                itemInfo['AppInfo']  = self._publishDashboard(config=appDet,
                                                               replaceInfo=replaceInfo)
            else:
                itemInfo['AppInfo']  = self._publishApp(config=appDet,
                                               replaceInfo=replaceInfo)

            if not itemInfo['AppInfo']  is None:
                if not 'error' in itemInfo['AppInfo']['Results'] :
                    print ("%s app created" % itemInfo['AppInfo']['Name'])
                else:
                    print (str(itemInfo['AppInfo']['Results']))
            else:
                print ("App was not created")
            return itemInfo

        except common.ArcRestHelperError as e:
            raise e
        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "_publishAppLogic",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
            })
        finally:
            replaceInfo = None
            replaceItem = None
            mapDet = None
            lay = None
            itemId = None
            admin = None

            del admin
            del replaceInfo
            del replaceItem
            del mapDet
            del lay
            del itemId
            gc.collect()
    #----------------------------------------------------------------------
    def publishApp(self, app_info, map_info=None, fsInfo=None):
        """Publishes apps to AGOL/Portal
        
        Args:
            app_info (list): A list of JSON configuration apps to publish.
            map_info (list): Defaults to ``None``.
            fsInfo (list): Defaults to ``None``.
        Returns:
            dict: A dictionary of results objects.
            
        """
        if self.securityhandler is None:
            print ("Security handler required")
            return
        appDet = None
        try:
            app_results = []
            if isinstance(app_info, list):
                for appDet in app_info:
                    app_results.append(self._publishAppLogic(appDet=appDet,map_info=map_info,fsInfo=fsInfo))
            else:
                app_results.append(self._publishAppLogic(appDet=app_info,map_info=map_info,fsInfo=fsInfo))
            return app_results

        except (common.ArcRestHelperError) as e:
            raise e
        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "publishApp",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
            })

        finally:
            appDet = None

            del appDet
            gc.collect()
    #----------------------------------------------------------------------
    def _publishApp(self, config, replaceInfo):
        resultApp = None
        name = None
        tags = None
        description = None
        extent = None
        itemJson = None
        admin = None

        json_data = None
        itemData = None
        replaceItem = None
        loc_df = None
        datestring = None
        snippet = None
        everyone = None
        org = None
        groupNames = None
        folderName = None
        url = None
        thumbnail = None
        itemType = None
        typeKeywords  = None
        itemParams = None
        userCommunity = None
        userContent = None
        res = None
        folderId = None
        folderContent = None
        itemId = None
        group_ids = None
        shareResults = None
        updateParams = None
        url = None
        updateResults = None
        portal = None
        try:
            resultApp = {'Results':{}}
            name = ''
            tags = ''
            description = ''
            extent = ''

            itemJson = config['ItemJSON']
            if os.path.exists(itemJson) == False:

                return {"Results":{"error": "%s does not exist" % itemJson}  }
            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            portalself = admin.portals.portalSelf

            if portalself.urlKey is None or portalself.customBaseUrl is None:
                parsedURL = urlparse.urlparse(url=self._securityHandler.org_url, scheme='', allow_fragments=True)
                orgURL = parsedURL.netloc + parsedURL.path
            else:
                orgURL =  portalself.urlKey + '.' +  portalself.customBaseUrl


            content = admin.content
            userInfo = content.users.user()
            userCommunity = admin.community

            folderName = config['Folder']
            if folderName is not None and folderName != "":
                if self.folderExist(name=folderName,folders=userInfo.folders) is None:
                    res = userInfo.createFolder(name=folderName)
                userInfo.currentFolder = folderName
            if 'id' in userInfo.currentFolder:
                folderId = userInfo.currentFolder['id']

            if os.path.exists(itemJson):
                with open(itemJson) as json_data:
                    try:
                        itemData = json.load(json_data)
                    except:
                        raise ValueError("%s is not a valid JSON File" % itemJson)

                    for replaceItem in replaceInfo:
                        if replaceItem['ReplaceType'] == 'Map' and 'ItemID' in replaceItem:
                            if 'values' in itemData:
                                if 'webmap' in itemData['values']:
                                    if itemData['values']['webmap'] == replaceItem['SearchString']:
                                        itemData['values']['webmap'] = replaceItem['ItemID']
                                        if 'folderId' in itemData:
                                            itemData['folderId'] = replaceItem['ItemFolder']
                            if 'map' in itemData:
                                if 'itemId' in itemData['map']:
                                    if itemData['map']['itemId'] == replaceItem['SearchString']:
                                        itemData['map']['itemId'] = replaceItem['ItemID']
                        elif replaceItem['ReplaceType'] == 'Layer' and 'ReplaceString' in replaceItem:
                            itemData = common.find_replace(itemData,replaceItem['SearchString'],replaceItem['ReplaceString'])
                        elif replaceItem['ReplaceType'] == 'Folder':
                            if 'id' in  userInfo.currentFolder:
                                folderID = userInfo.currentFolder['id']
                            else:
                                folderID = None
                            itemData = common.find_replace(itemData,replaceItem['SearchString'],folderID)
                        elif replaceItem['ReplaceType'] == 'Org':

                            itemData = common.find_replace(itemData,replaceItem['SearchString'],orgURL)
                        elif replaceItem['ReplaceType'] == 'GeoService':
                            if 'geometry' in portalself.helperServices:
                                if 'url' in portalself.helperServices["geometry"]:

                                    itemData = common.find_replace(itemData,replaceItem['SearchString'],portalself.helperServices["geometry"]['url'])
                        elif replaceItem['ReplaceType'] == 'Global':
                            itemData = common.find_replace(itemData,replaceItem['SearchString'],replaceItem['ReplaceString'])

            else:
                print ("%s does not exist." % itemJson)
                itemData = None

            name = config['Title']

            if 'DateTimeFormat' in config:
                loc_df = config['DateTimeFormat']
            else:
                loc_df = dateTimeFormat

            datestring = datetime.datetime.now().strftime(loc_df)
            name = name.replace('{DATE}',datestring)
            name = name.replace('{Date}',datestring)

            description = config['Description']
            tags = config['Tags']
            snippet = config['Summary']


            everyone = config['ShareEveryone']
            org = config['ShareOrg']
            groupNames = config['Groups']  #Groups are by ID. Multiple groups comma separated

            url = config['Url']
            thumbnail = config['Thumbnail']

            itemType = config['Type']
            typeKeywords = config['typeKeywords']

            itemParams = arcrest.manageorg.ItemParameter()
            itemParams.title = name
            itemParams.thumbnail = thumbnail
            itemParams.type = itemType

            itemParams.overwrite = True
            itemParams.description = description
            itemParams.tags = tags
            itemParams.snippet = snippet
            itemParams.description = description
            itemParams.typeKeywords = ",".join(typeKeywords)

            sea = arcrest.find.search(securityHandler=self._securityHandler)
            items = sea.findItem(title=name,
                                 itemType=
                                 ["Web Mapping Application",
                                  "Application"],
                                 searchorg=False)

            if items['total'] >= 1:
                for res in items['results']:
                    if 'type' in res and res['type'] == itemType:
                        if 'name' in res and res['name'] == name:
                            itemId = res['id']
                            break
                        if 'title' in res and res['title'] == name:
                            itemId = res['id']
                            break
            if not itemId is None:
                item = content.getItem(itemId).userItem
                results = item.updateItem(itemParameters=itemParams,
                                            text=json.dumps(itemData))

                if 'error' in results:
                    return results
                if item.ownerFolder != folderId:
                    if folderId is None:
                        folderId = "/"
                    moveRes = userInfo.moveItems(items=item.id,folder=folderId)
            else:
                try:
                    item = userInfo.addItem(
                            itemParameters=itemParams,
                            overwrite=True,
                            relationshipType=None,
                            originItemId=None,
                            destinationItemId=None,
                            serviceProxyParams=None,
                            metadata=None,
                            text=json.dumps(itemData))


                except Exception as e:
                    print (e)
            if item is None:
                return "App could not be added"

            group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
            shareResults = userInfo.shareItems(items=item.id,
                                               groups=','.join(group_ids),
                                               everyone=everyone,
                                               org=org)
            updateParams = arcrest.manageorg.ItemParameter()
            updateParams.title = name

            url = url.replace("{AppID}",item.id)
            url = url.replace("{OrgURL}",orgURL)
            #if portalself.urlKey is None or portalself.customBaseUrl is None:
                            #parsedURL = urlparse.urlparse(url=self._securityHandler.org_url, scheme='', allow_fragments=True)

            #else:
                            #url = url.replace("{OrgURL}", portalself.urlKey + '.' +  portalself.customBaseUrl)
            updateParams.url = url
            updateResults = item.updateItem(itemParameters=updateParams)

            resultApp['Results']['itemId'] = item.id
            resultApp['folderId'] = folderId
            resultApp['Name'] = name
            return resultApp


        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "_publishApp",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
            })

        finally:

            name = None
            tags = None
            description = None
            extent = None
            itemJson = None
            admin = None
            adminusercontent = None
            json_data = None
            itemData = None
            replaceItem = None
            loc_df = None
            datestring = None
            snippet = None
            everyone = None
            org = None
            groupNames = None
            folderName = None
            url = None
            thumbnail = None
            itemType = None
            typeKeywords  = None

            itemParams = None
            userCommunity = None
            userContent = None
            res = None
            folderId = None
            folderContent = None
            itemId = None
            group_ids = None
            shareResults = None
            updateParams = None
            url = None
            updateResults = None
            portal = None

            del name
            del portal
            del tags
            del description
            del extent
            del itemJson
            del admin
            del adminusercontent
            del json_data
            del itemData
            del replaceItem
            del loc_df
            del datestring
            del snippet
            del everyone
            del org
            del groupNames
            del folderName
            del url
            del thumbnail
            del itemType
            del typeKeywords
            del itemParams
            del userCommunity
            del userContent
            del res
            del folderId
            del folderContent
            del itemId
            del group_ids
            del shareResults
            del updateParams

            del updateResults

            gc.collect()
    #----------------------------------------------------------------------
    def _publishDashboard(self, config, replaceInfo):
        resultApp = None
        tags = None
        description = None
        extent = None
        itemJson = None
        layerIDSwitch = None
        admin = None
        adminusercontent = None
        json_data = None
        itemData = None
        replaceItem = None
        item = None
        response = None
        layerNamesID = None
        layerIDs = None
        tableNamesID = None
        tableIDs = None
        opLayer = None
        widget = None
        widgets = None
        mapTool = None
        dataSource = None
        configFileAsString = None
        repl = None
        name = None
        loc_df = None
        datestring = None
        snippet = None
        everyone  = None
        org  = None
        groupNames = None
        folderName = None
        thumbnail = None
        itemType = None
        typeKeywords = None
        itemParams = None
        adminusercontent = None
        userCommunity = None
        userContent = None
        folderId = None
        res = None
        folderContent = None
        itemId = None
        group_ids = None
        shareResults = None
        updateParams = None
        resultApp = None
        updateResults = None
        try:
            resultApp = {'Results':{}}

            tags = ''
            description = ''
            extent = ''


            itemJson = config['ItemJSON']
            if os.path.exists(itemJson) == False:
                return {"Results":{"error": "%s does not exist" % itemJson}  }

            admin = arcrest.manageorg.Administration(securityHandler=self._securityHandler)
            content = admin.content
            userInfo = content.users.user()
            userCommunity = admin.community
            folderName = config['Folder']
            if folderName is not None and folderName != "":
                if self.folderExist(name=folderName,folders=userInfo.folders) is None:
                    res = userInfo.createFolder(name=folderName)
                    userInfo.refresh()
                userInfo.currentFolder = folderName
            if 'id' in userInfo.currentFolder:
                folderId = userInfo.currentFolder['id']

            layerIDSwitch = []

            if os.path.exists(itemJson):
                with open(itemJson) as json_data:
                    try:
                        itemData = json.load(json_data)
                    except:
                        raise ValueError("%s is not a valid JSON File" % itemJson)

                    for replaceItem in replaceInfo:
                        if replaceItem['ReplaceType'] == 'Global':
                            itemData = common.find_replace(itemData,replaceItem['SearchString'],replaceItem['ReplaceString'])
                        elif replaceItem['ReplaceType'] == 'Map' and 'ItemID' in replaceItem:
                            item = admin.content.getItem(itemId=replaceItem['ItemID'])
                            response = item.itemData()

                            layerNamesID = {}
                            layerIDs =[]

                            tableNamesID = {}
                            tableIDs =[]

                            if 'operationalLayers' in response:
                                for opLayer in response['operationalLayers']:
                                    #if 'LayerInfo' in replaceItem:
                                        #for layers in replaceItem['LayerInfo']:
                                    layerNamesID[opLayer['title']] = opLayer['id']
                                    layerIDs.append(opLayer['id'])
                            if 'tables' in response:
                                for opLayer in response['tables']:
                                    tableNamesID[opLayer['title']] = opLayer['id']
                                    tableIDs.append(opLayer['id'])

                            widgets = itemData['widgets']
                            dataSourceIDToFields = {}
                            for widget in widgets:

                                if 'mapId' in widget:
                                    if replaceItem['SearchString'] == widget['mapId']:
                                        widget['mapId'] = replaceItem['ItemID']
                                        if 'mapTools' in widget:
                                            for mapTool in widget['mapTools']:
                                                if 'layerIds' in mapTool:
                                                    mapTool['layerIds'] = layerIDs
                                        if 'dataSources' in widget:
                                            for dataSource in widget['dataSources']:

                                                if 'layerId' in dataSource:
                                                    if 'LayerInfo' in replaceItem:
                                                        if dataSource['layerId'] in replaceItem['LayerInfo']:
                                                            layerIDSwitch.append({"OrigID":dataSource['layerId'],
                                                                                  "NewID":replaceItem['LayerInfo'][dataSource['layerId']]['ID']})
                                                                                  #'FieldInfo':replaceItem['LayerInfo'][dataSource['layerId']]['FieldInfo']})

                                                            #dataSourceIDToFields[dataSource['id']] = {'NewID': replaceItem['LayerInfo'][dataSource['layerId']]['ID'],
                                                                                                      #'FieldInfo': replaceItem['LayerInfo'][dataSource['layerId']]['FieldInfo']}
                                                            dataSource['layerId'] = replaceItem['LayerInfo'][dataSource['layerId']]['ID']
                                                    elif dataSource['name'] in layerNamesID:
                                                        layerIDSwitch.append({"OrigID":dataSource['layerId'],"NewID":layerNamesID[dataSource['name']] })
                                                        dataSource['layerId'] = layerNamesID[dataSource['name']]
                                            for dataSource in widget['dataSources']:

                                                if 'filter' in dataSource:
                                                    if dataSource['parentDataSourceId'] in dataSourceIDToFields:
                                                        if 'whereClause' in dataSource['filter']:
                                                            whercla = str(dataSource['filter']['whereClause'])
                                                            if pyparsingInstall:
                                                                try:
                                                                    selectResults = select_parser.select_stmt.parseString("select * from xyzzy where " + whercla)

                                                                    whereElements = list(selectResults['where_expr'])
                                                                    for h in range(len(whereElements)):
                                                                        for field in dataSourceIDToFields[dataSource['parentDataSourceId']]['FieldInfo']['fields']:
                                                                            if whereElements[h] == field['PublishName']:
                                                                                whereElements[h] = field['ConvertName']
                                                                                #whercla = whercla.replace(
                                                                                    #old=field['PublishName'],
                                                                                    #new=field['ConvertName'])
                                                                    dataSource['filter']['whereClause'] = " ".join(whereElements)
                                                                except select_parser.ParseException as pe:
                                                                    for field in dataSourceIDToFields[dataSource['parentDataSourceId']]['FieldInfo']['fields']:
                                                                        if whercla.contains(field['PublishName']):
                                                                            whercla = whercla.replace(
                                                                                old=field['PublishName'],
                                                                                new=field['ConvertName'])


                                                            else:

                                                                for field in dataSourceIDToFields[dataSource['parentDataSourceId']]['FieldInfo']['fields']:
                                                                    if whercla.contains(field['PublishName']):
                                                                        whercla = whercla.replace(
                                                                                       old=field['PublishName'],
                                                                                       new=field['ConvertName'])




            configFileAsString = json.dumps(itemData)
            for repl in layerIDSwitch:
                configFileAsString.replace(repl['OrigID'],repl['NewID'])

            itemData = json.loads(configFileAsString)


            name = config['Title']

            if 'DateTimeFormat' in config:
                loc_df = config['DateTimeFormat']
            else:
                loc_df = dateTimeFormat

            datestring = datetime.datetime.now().strftime(loc_df)
            name = name.replace('{DATE}',datestring)
            name = name.replace('{Date}',datestring)

            description = config['Description']
            tags = config['Tags']
            snippet = config['Summary']


            everyone = config['ShareEveryone']
            org = config['ShareOrg']
            groupNames = config['Groups']  #Groups are by ID. Multiple groups comma separated

            folderName = config['Folder']
            thumbnail = config['Thumbnail']

            itemType = config['Type']
            typeKeywords = config['typeKeywords']

            itemParams = arcrest.manageorg.ItemParameter()
            itemParams.title = name
            itemParams.thumbnail = thumbnail
            itemParams.type = itemType

            itemParams.overwrite = True
            itemParams.description = description
            itemParams.snippet = snippet
            itemParams.typeKeywords = ",".join(typeKeywords)

            sea = arcrest.find.search(securityHandler=self._securityHandler)
            items = sea.findItem(title=name, itemType=
                                 ["Web Mapping Application",
                                  "Application",
                                  "Operation View"],
                                 searchorg=False)

            if items['total'] >= 1:
                for res in items['results']:
                    if 'type' in res and res['type'] == itemType:
                        if 'name' in res and res['name'] == name:
                            itemId = res['id']
                            break
                        if 'title' in res and res['title'] == name:
                            itemId = res['id']
                            break
            if not itemId is None:
                item = content.getItem(itemId).userItem
                results = item.updateItem(itemParameters=itemParams,
                                                       text=json.dumps(itemData))
                if 'error' in results:
                    return results
                if item.ownerFolder != folderId:
                    if folderId is None:
                        folderId = "/"
                    moveRes = userInfo.moveItems(items=item.id,folder=folderId)
            else:
                try:

                    item = userInfo.addItem(
                        itemParameters=itemParams,
                        relationshipType=None,
                        originItemId=None,
                        destinationItemId=None,
                        serviceProxyParams=None,
                        metadata=None,
                        text=json.dumps(itemData))
                except Exception as e:
                    print (e)

            if item is None:
                return "Dashboard could not be added"
            group_ids = userCommunity.getGroupIDs(groupNames=groupNames)
            shareResults = userInfo.shareItems(items=item.id,
                                               groups=','.join(group_ids),
                                               everyone=everyone,
                                               org=org)
            updateParams = arcrest.manageorg.ItemParameter()
            updateParams.title = name

            updateResults = item.updateItem(itemParameters=updateParams)
            resultApp['Results']['itemId'] = item.id

            resultApp['folderId'] = folderId
            resultApp['Name'] = name
            return resultApp


        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "_publishDashboard",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
            })
        finally:

            tags = None
            description = None
            extent = None
            itemJson = None
            layerIDSwitch = None
            admin = None
            adminusercontent = None
            json_data = None
            itemData = None
            replaceItem = None
            item = None
            response = None
            layerNamesID = None
            layerIDs = None
            tableNamesID = None
            tableIDs = None
            opLayer = None
            widget = None
            widgets = None
            mapTool = None
            dataSource = None
            configFileAsString = None
            repl = None
            name = None
            loc_df = None
            datestring = None
            snippet = None
            everyone  = None
            org  = None
            groupNames = None
            folderName = None
            thumbnail = None
            itemType = None
            typeKeywords = None
            itemParams = None
            adminusercontent = None
            userCommunity = None
            userContent = None
            folderId = None
            res = None
            folderContent = None
            itemId = None
            group_ids = None
            shareResults = None
            updateParams = None

            updateResults = None


            del tags
            del description
            del extent
            del itemJson
            del layerIDSwitch
            del admin

            del json_data
            del itemData
            del replaceItem
            del item
            del response
            del layerNamesID
            del layerIDs
            del tableNamesID
            del tableIDs
            del opLayer
            del widget
            del widgets
            del mapTool
            del dataSource
            del configFileAsString
            del repl
            del name
            del loc_df
            del datestring
            del snippet
            del everyone
            del org
            del groupNames
            del folderName
            del thumbnail
            del itemType
            del typeKeywords
            del itemParams
            del adminusercontent
            del userCommunity
            del userContent
            del folderId
            del res
            del folderContent
            del itemId
            del group_ids
            del shareResults
            del updateParams

            del updateResults
            gc.collect()
    #----------------------------------------------------------------------
    def updateFeatureService(self, efs_config):
        """Updates a feature service.
        
        Args:
            efs_config (list): A list of JSON configuration feature service details to update.
        Returns:
            dict: A dictionary of results objects.
        
        """
        if self.securityhandler is None:
            print ("Security handler required")
            return
        fsRes = None
        fst = None
        fURL = None
        resItm= None
        try:

            fsRes = []
            fst = featureservicetools.featureservicetools(securityinfo=self)


            if isinstance(efs_config, list):
                for ext_service in efs_config:
                    fURL = None
                    cs = 0
                    try:
                        if 'ChunkSize' in ext_service:
                            if common.is_number(ext_service['ChunkSize']):
                                cs = ext_service['ChunkSize']
                    except Exception as e:
                        pass
                    resItm={"DeleteDetails": None,"AddDetails":None}
                    if 'ItemId' in ext_service and 'LayerName' in ext_service:
                        fs = fst.GetFeatureService(itemId=ext_service['ItemId'],returnURLOnly=False)
                        if not fs is None:
                            fURL = fst.GetLayerFromFeatureService(fs=fs,layerName=ext_service['LayerName'],returnURLOnly=True)
                    if fURL is None and 'URL' in ext_service:

                        fURL = ext_service['URL']
                    if fURL is None:
                        print("Item and layer not found or URL not in config")
                        continue

                    if 'DeleteInfo' in ext_service:
                        if str(ext_service['DeleteInfo']['Delete']).upper() == "TRUE":
                            resItm['DeleteDetails'] = fst.DeleteFeaturesFromFeatureLayer(url=fURL, sql=ext_service['DeleteInfo']['DeleteSQL'],chunksize=cs)
                            if not 'error' in resItm['DeleteDetails'] :
                                print ("Delete Successful: %s" % fURL)
                            else:
                                print (str(resItm['DeleteDetails']))

                    resItm['AddDetails'] = fst.AddFeaturesToFeatureLayer(url=fURL, pathToFeatureClass = ext_service['FeatureClass'],chunksize=cs)

                    fsRes.append(resItm)

                    if not 'error' in resItm['AddDetails']:
                        print ("Add Successful: %s " % fURL)
                    else:
                        print (str(resItm['AddDetails']))

            else:
                resItm={"DeleteDetails": None,"AddDetails":None}
                fURL = efs_config['URL']
                cs = 0
                try:
                    if 'ChunkSize' in efs_config:
                        if common.is_number(efs_config['ChunkSize']):
                            cs = efs_config['ChunkSize']
                except Exception as e:
                    pass
                if 'ItemId' in efs_config and 'LayerName' in efs_config:
                    fs = fst.GetFeatureService(itemId=efs_config['ItemId'],returnURLOnly=False)
                    if not fs is None:
                        fURL = fst.GetLayerFromFeatureService(fs=fs,layerName=efs_config['LayerName'],returnURLOnly=True)
                if fURL is None and 'URL' in efs_config:

                    fURL = efs_config['URL']
                if fURL is None:
                    print("Item and layer not found or URL not in config")
                    return None
                if 'DeleteInfo' in efs_config:
                    if str(efs_config['DeleteInfo']['Delete']).upper() == "TRUE":
                        resItm['DeleteDetails'] = fst.DeleteFeaturesFromFeatureLayer(url=fURL, sql=efs_config['DeleteInfo']['DeleteSQL'],chunksize=cs)
                        if not 'error' in resItm['DeleteDetails'] :
                            print ("            Delete Successful: %s" % fURL)
                        else:
                            print ("            " + str(resItm['DeleteDetails']))

                resItm['AddDetails'] = fst.AddFeaturesToFeatureLayer(url=fURL, pathToFeatureClass = efs_config['FeatureClass'],chunksize=cs)

                fsRes.append(resItm)

                if not 'error' in resItm['AddDetails']:
                    print ("            Add Successful: %s " % fURL)
                else:
                    print ("            " + str(resItm['AddDetails']))

            return fsRes

        except common.ArcRestHelperError as e:
            raise e
        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "updateFeatureService",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
            })
        finally:
            fst = None
            fURL = None
            resItm= None

            del fst
            del fURL
            del resItm

            gc.collect()
    #----------------------------------------------------------------------
    def _publishFeatureCollection(self, config):
        try:

            # Service settings
            zipfile = config['Zip']
            service_name = config['Title']
            if 'DateTimeFormat' in config:
                loc_df = config['DateTimeFormat']
            else:
                loc_df = dateTimeFormat

            description = ""
            if 'Description' in config:
                description = config['Description']

            tags = config['Tags']
            snippet = config['Summary']
            extent = config['Extent']

            everyone = config['ShareEveryone']
            org = config['ShareOrg']
            groupNames = config['Groups']  #Groups are by ID. Multiple groups comma separated

            folderName = config['Folder']
            thumbnail = config['Thumbnail']

            typeKeywords = config['typeKeywords']

            datestring = datetime.datetime.now().strftime(loc_df)
            service_name = service_name.replace('{DATE}',datestring)
            service_name = service_name.replace('{Date}',datestring)

            service_name_safe = service_name.replace(' ','_')
            service_name_safe = service_name_safe.replace(':','_')
            service_name_safe = service_name_safe.replace('-','_')

            if os.path.exists(path=zipfile) == False:
                raise ValueError("Zip does not exit")

            admin = arcrest.manageorg.Administration(securityHandler=self.securityhandler)
            content = admin.content
            feature_content = content.FeatureContent

            publishParameters = arcrest.manageorg.GenerateParameter(
                name=service_name,maxRecordCount=4000
                )


            fcResults = feature_content.generate(publishParameters=publishParameters,
                itemId=None,
                filePath=zipfile,
                fileType='shapefile')

            if not 'featureCollection' in fcResults:
                raise common.ArcRestHelperError({
                    "function": "_publishFeatureCollection",
                    "line": lineno(),
                    "filename":  'publishingtools.py',
                    "synerror": fcResults
                })
            if not 'layers' in fcResults['featureCollection']:
                raise common.ArcRestHelperError({
                    "function": "_publishFeatureCollection",
                    "line": lineno(),
                    "filename":  'publishingtools.py',
                    "synerror": fcResults
                })

            fcJson = {'visibility':True,
                      'showLegend':True,
                      'opacity':1}
            for layer in fcResults['featureCollection']['layers']:
                oidFldName = ''
                highOID = -1
                popInfo = {'title':'',
                           'description':None,
                           'showAttachments': False,
                           'mediaInfo': [],
                           'fieldInfos': []
                           }
                if 'layerDefinition' in layer:
                    extVal = extent.split(',')
                    layer['layerDefinition']['extent'] = {'type':'extent',
                                       'xmin':extVal[0],
                                       'ymin':extVal[1],
                                       'xmax':extVal[2],
                                       'ymax':extVal[3]
                                       }
                    layer['layerDefinition']['spatialReference'] = {'wkid':102100}

                    if 'fields' in layer['layerDefinition']:
                        for field in layer['layerDefinition']['fields']:
                            fieldInfos = None
                            if field['type'] == 'esriFieldTypeOID':
                                oidFldName = field['name']
                                fieldInfos = {
                                    'fieldName':field['name'],
                                    'label':field['alias'],
                                    'isEditable':False,
                                    'tooltip':'',
                                    'visible':False,
                                    'format':None,
                                    'stringFieldOption':'textbox'
                                }

                            elif field['type'] == 'esriFieldTypeInteger':
                                fieldInfos = {
                                    'fieldName':field['name'],
                                    'label':field['alias'],
                                    'isEditable':True,
                                    'tooltip':'',
                                    'visible':True,
                                    'format':{
                                        'places':0,
                                        'digitSeparator':True
                                    },
                                    'stringFieldOption':'textbox'
                                }
                            elif field['type'] == 'esriFieldTypeDouble':
                                fieldInfos = {
                                    'fieldName':field['name'],
                                    'label':field['alias'],
                                    'isEditable':True,
                                    'tooltip':'',
                                    'visible':True,
                                    'format':{
                                        'places':2,
                                        'digitSeparator':True
                                        },
                                    'stringFieldOption':'textbox'
                                }
                            elif field['type'] == 'esriFieldTypeString':
                                fieldInfos = {
                                    'fieldName':field['name'],
                                    'label':field['alias'],
                                    'isEditable':True,
                                    'tooltip':'',
                                    'visible':True,
                                    'format':None,
                                    'stringFieldOption':'textbox'
                                }
                            else:
                                fieldInfos = {
                                    'fieldName':field['name'],
                                    'label':field['alias'],
                                    'isEditable':True,
                                    'tooltip':'',
                                    'visible':True,
                                    'format':None,
                                    'stringFieldOption':'textbox'
                                }
                            if fieldInfos is not None:
                                popInfo['fieldInfos'].append(fieldInfos)

                if 'featureSet' in layer:
                    if 'features' in layer['featureSet']:
                        for feature in layer['featureSet']['features']:
                            if 'attributes' in feature:
                                if feature['attributes'][oidFldName] > highOID:
                                    highOID = feature[oidFldName]
                layer['nextObjectId'] = highOID + 1

            fcJson['layers'] = fcResults['featureCollection']['layers']
            itemParams = arcrest.manageorg.ItemParameter()
            itemParams.type = "Feature Collection"
            itemParams.title = service_name
            itemParams.thumbnail = thumbnail
            itemParams.overwrite = True
            itemParams.snippet = snippet
            itemParams.description = description
            itemParams.extent = extent
            itemParams.tags = tags
            itemParams.typeKeywords = ",".join(typeKeywords)

            userInfo = content.users.user()
            userCommunity = admin.community


            if folderName is not None and folderName != "":
                if self.folderExist(name=folderName,folders=userInfo.folders) is None:
                    res = userInfo.createFolder(name=folderName)
                userInfo.currentFolder = folderName
            if 'id' in userInfo.currentFolder:
                folderId = userInfo.currentFolder['id']

            sea = arcrest.find.search(securityHandler=self._securityHandler)
            items = sea.findItem(title=service_name, itemType='Feature Collection',searchorg=False)
            itemId = None
            if items['total'] >= 1:
                for res in items['results']:
                    if 'type' in res and res['type'] == 'Feature Collection':
                        if 'name' in res and res['name'] == service_name:
                            itemId = res['id']
                            break
                        if 'title' in res and res['title'] == service_name:
                            itemId = res['id']
                            break
            if not itemId is None:
                item = content.getItem(itemId).userItem
                resultSD = item.updateItem(itemParameters=itemParams,
                                           text=fcJson)
                if item.ownerFolder != folderId:
                    if folderId is None:
                        folderId = "/"
                    moveRes = userInfo.moveItems(items=item.id,folder=folderId)
            else:

                resultSD = userInfo.addItem(itemParameters=itemParams,
                                            overwrite=True,
                                            url=None,
                                            text= fcJson,
                                            relationshipType=None,
                                            originItemId=None,
                                            destinationItemId=None,
                                            serviceProxyParams=None,
                                            metadata=None)



            if 'error' in resultSD:
                if not itemId is None:
                    print ("Attempting to delete")
                    delres=userInfo.deleteItems(items=itemId)
                    if 'error' in delres:
                        print (delres)
                        return delres
                    print ("Delete successful")
                else:
                    print ("Item exist and cannot be found, probably owned by another user.")
                    raise common.ArcRestHelperError({
                        "function": "_publishFeatureCollection",
                        "line": lineno(),
                        "filename":  'publishingtools.py',
                        "synerror": "Item exist and cannot be found, probably owned by another user."
                    })

                resultSD = userInfo.addItem(itemParameters=itemParams,
                                            overwrite=True,
                                            url=None,
                                            text=fcResults['featureCollection'],
                                            relationshipType=None,
                                            originItemId=None,
                                            destinationItemId=None,
                                            serviceProxyParams=None,
                                            metadata=None)
                return resultSD
            else:
                return resultSD




        except common.ArcRestHelperError as e:
            raise e

        except Exception as e:

            line, filename, synerror = trace()
            raise common.ArcRestHelperError({
                "function": "_publishFeatureCollection",
                "line": line,
                "filename":  filename,
                "synerror": synerror,
            })
        finally:


            gc.collect()
