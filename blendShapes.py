import maya.cmds as cmds
import maya.api.OpenMaya as om2
import logging

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

def targetIndex(bsNode,targetName):
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

def removeBlendshape():
    pass
