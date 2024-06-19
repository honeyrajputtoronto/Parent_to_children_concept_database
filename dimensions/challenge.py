from .models import Company, Dimension
from django.core.cache import cache
from django.core import serializers

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

def get_company_id_from_root(root_id):
    try:
        root_dimension = Dimension.objects.select_related('company').get(id=root_id)
        return root_dimension.company_id
    except Dimension.DoesNotExist:
        return None

def list_children(company_id):
    try:
        cache_key = f"company_{company_id}_dimensions"
        cached_data = cache.get(cache_key)

        if cached_data:
            all_dimensions = [dim.object for dim in serializers.deserialize('json', cached_data)]
        else:
            all_dimensions = list(Dimension.objects.filter(company_id=company_id).select_related('parent', 'company'))
            serialized_data = serializers.serialize('json', all_dimensions)
            cache.set(cache_key, serialized_data, timeout=3600)
            all_dimensions = [dim.object for dim in serializers.deserialize('json', serialized_data)]  # Extract objects from deserialized data

        root_dimension = next((dim for dim in all_dimensions if dim.id == company_id), None)
        if not root_dimension:
            return None

        parent_to_children = collect_parent_to_children(all_dimensions)
        result = traverse(root_dimension, parent_to_children)
        return result

    except Dimension.DoesNotExist:
        return None


def list_hierarchy(company_id):
    try:
        cache_key = f"company_{company_id}_dimensions"
        cached_data = cache.get(cache_key)

        if cached_data:
            all_dimensions = [dim.object for dim in serializers.deserialize('json', cached_data)]
        else:
            all_dimensions = list(Dimension.objects.filter(company_id=company_id).select_related('parent', 'company'))
            serialized_data = serializers.serialize('json', all_dimensions)
            cache.set(cache_key, serialized_data, timeout=3600)
            all_dimensions = [dim.object for dim in serializers.deserialize('json', serialized_data)]  # Extract objects from deserialized data

        parent_to_children = collect_parent_to_children(all_dimensions)
        top_level_dimensions = [dim for dim in all_dimensions if dim.parent_id is None]
        result = traverse(top_level_dimensions, parent_to_children)
        return result

    except Company.DoesNotExist:
        return None