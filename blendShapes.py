import maya.cmds as cmds
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as OpenMayaAnim2
from openMaya import transformUtils


def isBlendshape(blendshapeName):
    """

    :param blendshapeName: name of the blendshapeNode
    :return:
    """
    if not cmds.objExists(blendshapeName):
        return False

    if not cmds.objectType(blendshapeName) == "blendShape":
        return False
    return True

def getTargetIndex(bsNode,targetName):
    """

    :param bsNode:name of blendshape node
    :param targetName:name of target
    :return:target index number
    """
    aliasList=cmds.aliasAttr(bsNode, q=True)
    aliasIndex=aliasList.index(targetName)
    aliasAttr=aliasList[aliasIndex+1]
    targetIndex=int(aliasAttr.split("[")[-1].split("]")[0])
    return targetIndex

def getBaseGeometryIndexFromDeformer(deformer,base):
    """

    :param deformer:
    :param base:
    :return:
    """
    mDeformObj = transformUtils.getmObject(deformer)
    if cmds.objectType(base) == "transform":
        base = cmds.listRelatives(base, s=True, ni=True, pa=True)[0]
    baseObj=transformUtils.getmObject(base)

    deformFn = OpenMayaAnim2.MFnGeometryFilter(mDeformObj)
    geoIndex = deformFn.indexForOutputShape(baseObj)
    return geoIndex

def getTargetGeo(bsNode, baseGeo, target):
    """

    :param bsNode:
    :param baseGeo:
    :param target:
    :return:
    """
    targetIndex = getTargetIndex(bsNode, target)
    geoIndex =getBaseGeometryIndexFromDeformer(bsNode, baseGeo)
    targetConnectAttr = "{0}.inputTarget[{1}].inputTargetGroup[{2}].inputTargetItem[6000].inputGeomTarget".format(
                         bsNode, geoIndex, targetIndex)
    targetGeo = cmds.listConnections(targetConnectAttr, s=True, d=False)[0]
    if cmds.objExists(targetGeo):
        return targetGeo
    else:
        raise Exception ("target geo doesnt exist")


def connectTargetGeo(bsNode, baseGeo, targetName , targetGeo ,force=True ):
    targetIndex = getTargetIndex(bsNode, targetName)
    geoIndex = getBaseGeometryIndexFromDeformer(bsNode, baseGeo)
    targetConnectAttr = "{0}.inputTarget[{1}].inputTargetGroup[{2}].inputTargetItem[6000].inputGeomTarget".format(
        bsNode, geoIndex, targetIndex)

    targetGeoShape = cmds.listRelatives(targetGeo, s=1, ni=1, pa=1)[0]
    attrType = cmds.objectType(targetGeoShape)
    shapeAttrDict = {"mesh": "worldMesh[0]", "nurbsSurface": "worldSpace[0]", "nurbsCurve": "worldSpace[0]"}
    if shapeAttrDict.has_key(attrType):
        cmds.connectAttr("{}.{}".format(targetGeoShape, shapeAttrDict[attrType]), targetConnectAttr, f=force)




def removeBlendshape(bsNode, baseGeo, targetName , targetGeo ,deleteTarget=False):
    targetIndex = getTargetIndex(bsNode, targetName)
    if not cmds.objExists(targetGeo):
        deleteTarget=True
        targetGeo=cmds.duplicate(baseGeo,n=targetGeo)[0]
        connectTargetGeo(bsNode, baseGeo, targetName, targetGeo, force=True)
    cmds.blendShape(bsNode, edit=True, rm=True, t=(baseGeo, targetIndex, targetGeo, 1.0))
    if deleteTarget:
        cmds.delete(targetGeo)



