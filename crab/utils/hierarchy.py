"""
This contains a series of utility and helper functions which do not
live under any bespoke module
"""
from .. import config


# ------------------------------------------------------------------------------
def get_between(from_this, to_this, inclusive=True):

    # -- Ensure that the two objects are in the same hierarchy
    if from_this.name() not in to_this.longName():
        raise Exception(
            '%s is not in the same hierarchy as %s' % (
                from_this,
                to_this,
            ),
        )
    # -- Create a list to track
    joints_between = [to_this]

    while True:

        # -- Add the parent of the last added joints
        joints_between.append(joints_between[-1].getParent())

        # -- If the last item is the start item we can break out
        if joints_between[-1] == from_this:
            break

    if not inclusive:
        joints_between = joints_between[1:-1]

    # -- Reverse the order so its top down
    joints_between.reverse()

    return joints_between


# ------------------------------------------------------------------------------
def find_below(node, substring):
    """
    Looks for the first immediate child with the given substring in the name

    :param node: Node to search from
    :type node: pm.nt.DagNode

    :param substring: String to look for in a node name
    :type substring: str

    :return: pm.nt.DagNode
    """
    for child in node.getChildren():
        if substring in child.name():
            return child

    return None


# ------------------------------------------------------------------------------
def find_above(node, substring):
    """
    Looks for the parent with the given substring in the name

    :param node: Node to search from
    :type node: pm.nt.DagNode

    :param substring: String to look for in a node name
    :type substring: str

    :return: pm.nt.DagNode
    """
    while node:
        if substring in node.name():
            return node

        node = node.getParent()

    return None


# ------------------------------------------------------------------------------
def get_offset(node):
    """
    Looks for the offset parent for the given node

    :param node: Node to search from
    :type node: pm.nt.DagNode

    :return: pm.nt.DagNode
    """
    return find_above(node, config.OFFSET)


# ------------------------------------------------------------------------------
def get_zero(node):
    """
    Looks for the zero parent for the given node

    :param node: Node to search from
    :type node: pm.nt.DagNode

    :return: pm.nt.DagNode
    """
    return find_above(node, config.ZERO)


# ------------------------------------------------------------------------------
def get_org(node):
    """
    Looks for the org parent for the given node

    :param node: Node to search from
    :type node: pm.nt.DagNode

    :return: pm.nt.DagNode
    """
    return find_above(node, config.ORG)


# -----------------------------------------------------
def get_driving_control(skeletal_joint):
    """
    Returns the control designated as driving (binding) this joint.

    :param skeletal_joint: The joint to find the control for
    :type skeletal_joint: pm.nt.Joint

    :return: pm.nt.Transform
    """
    if skeletal_joint.hasAttr(config.BOUND):
        for potential in skeletal_joint.attr(config.BOUND).inputs():
            return potential

    return None
