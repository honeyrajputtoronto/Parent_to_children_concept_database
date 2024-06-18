from .models import Company, Dimension
from django.core.cache import cache
import json
from django.db import connection


def collect_parent_to_children(all_dimensions):
    parent_to_children = {}
    for dimension in all_dimensions:
        parent_id = dimension.parent_id
        if parent_id not in parent_to_children:
            parent_to_children[parent_id] = []
        parent_to_children[parent_id].append(dimension)
    return parent_to_children


def traverse(dimensions, parent_to_children, level=0):
    if not isinstance(dimensions, list):
        dimensions = [dimensions]
    result = []
    for dimension in dimensions:
        children = parent_to_children.get(dimension.id, [])
        indentation = '\t' * level
        res = f"{indentation}{dimension.name}"
        result.append(res)
        if children:
            result.extend(traverse(children, parent_to_children, level + 1))
    return result


def list_children(root_id):
    try:
        root_dimension = Dimension.objects.select_related('parent', 'company').get(id=root_id)
        all_dimensions = Dimension.objects.select_related('parent', 'company').all()
        parent_to_children = collect_parent_to_children(all_dimensions)
        result = traverse(root_dimension, parent_to_children)
        return result
    except Dimension.DoesNotExist:
        return None


def list_hierarchy(root_id):
    try:
        dimensions = Dimension.objects.filter(company=root_id).select_related('parent', 'company')
        parent_to_children = collect_parent_to_children(dimensions)
        top_level_dimensions = [dim for dim in dimensions if dim.parent_id is None]
        result = traverse(top_level_dimensions, parent_to_children)
        return result
    except Company.DoesNotExist:
        return None
