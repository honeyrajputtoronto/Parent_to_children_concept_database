from .models import Company, Dimension
from django.core.cache import cache
import json

def collect_parent_to_children(all_dimension):
    parent_to_children = {}
    for dimension in all_dimension:
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
        # print('dimension', dimension)
        children = parent_to_children.get(dimension.id, [])
        indentation = '\t' * level
        res = f"{indentation}{dimension.name}"
        result.append(res)
        if children:
            result.extend(traverse(children, parent_to_children, level + 1))
            if dimension.parent == None:
                cache_key = f"dimension_hierarchy_{dimension.id}"
                hierarchy = cache.get(cache_key)
                print('---------hierarchy-------', hierarchy, '-----cache key-----',cache_key)
    return result

def list_children(root_id):
    # print('root_id', root_id)
    # cache_key = f"dimension_hierarchy_{root_id}"
    # hierarchy = cache.get(cache_key)
    # # print('cache key----', cache_key)
    # # print('hierarchy', hierarchy)
    # if hierarchy:
    #     print(f"Cache hit for {cache_key}")
    #     return json.loads(hierarchy)
    # else:
    #     print(f"Cache miss for {cache_key}")

    try:
        root_dimension = Dimension.objects.select_related('parent', 'company').get(id=root_id)
        print('children root_dimension...', root_dimension)
        all_dimension = Dimension.objects.select_related('parent', 'company').all()
        print('children all dimensions ',all_dimension)
        parent_to_children = collect_parent_to_children(all_dimension)
        # print('root_dimension...',root_dimension)
        # print('parent_to_children...', parent_to_children)
        result = traverse(root_dimension, parent_to_children)
        # cache.set(cache_key, json.dumps(result), timeout=3600)  # Cache for 1 hour
        # hierarchy = cache.get(cache_key)
        # print('hierarchy = cache.get(cache_key)', hierarchy)
        return result
    except Dimension.DoesNotExist:
        print('Root Dimension does not exist.')
        return None

def list_hierarchy(root_id):
    cache_key = f"company_hierarchy_{root_id}"
    hierarchy = cache.get(cache_key)
    if hierarchy:
        print(f"Cache hit for {cache_key}")
        return json.loads(hierarchy)
    else:
        print(f"Cache miss for {cache_key}")

    try:
        company = Company.objects.get(id=root_id)
        dimensions = Dimension.objects.filter(company=company).select_related('parent', 'company')
        parent_to_children = collect_parent_to_children(dimensions)
        top_level_dimensions = [dim for dim in dimensions if dim.parent_id is None]
        # print('top_level_dimensions', top_level_dimensions)
        # print('parent_to_children', parent_to_children)
        result = traverse(top_level_dimensions, parent_to_children)
        cache.set(cache_key, json.dumps(result), timeout=3600)  # Cache for 1 hour
        return result
    except Company.DoesNotExist:
        print('Company does not exist')
        return None

    # # new
    # top_level_dimensions = [dim for dim in dimensions if dim.parent_id is None]
    # for level in top_level_dimensions:


# def get_cached_hierarchy(company_id):
#     cache_key = f"company_hierarchy_{company_id}"
#     hierarchy = cache.get(cache_key)
#     if not hierarchy:
#         hierarchy = list_hierarchy(company_id)
#         cache.set(cache_key, json.dumps(hierarchy), timeout=3600)  # Cache for 1 hour
#     else:
#         hierarchy = json.loads(hierarchy)
#     return hierarchy

# def get_fragmented_hierarchy(dimension_id):
#     cache_key = f"dimension_hierarchy_{dimension_id}"
#     hierarchy = cache.get(cache_key)
#     if not hierarchy:
#         hierarchy = list_children(dimension_id)
#         cache.set(cache_key, json.dumps(hierarchy), timeout=3600)  # Cache for 1 hour
#     return hierarchy

from celery import shared_task

@shared_task
def refresh_hierarchy_cache(company_id):
    dimensions = list(Dimension.objects.filter(company_id=company_id).select_related('parent', 'company'))
    parent_to_children = collect_parent_to_children(dimensions)
    top_level_dimensions = [dim for dim in dimensions if dim.parent_id is None]
    hierarchy = traverse(top_level_dimensions, parent_to_children)
    cache.set(f"company_hierarchy_{company_id}", json.dumps(hierarchy), timeout=3600)

# def update_dimension(dimension):
#     dimension.save()
#     refresh_hierarchy_cache.delay(dimension.company_id)

# def delete_dimension(dimension):
#     company_id = dimension.company_id
#     dimension.delete()
#     refresh_hierarchy_cache.delay(company_id)


def add_new_dimension():
    # Adding a new dimension to check the working of cache system.
    company = Company.objects.get(pk=1)
    parent = Dimension.objects.get(pk=21)  # parent with pk=21
    new_dimension = Dimension(company=company, parent=parent, name="New", has_children=False)
    new_dimension.save()
    print('Object added:', new_dimension)

    # Find the root dimension
    root_dimension = find_root_dimension(parent)

    # Return the ID and name of the root dimension
    root_info =  root_dimension.id, root_dimension.name

    root_id = root_info[0]
    return root_id


def find_root_dimension(dimension):
    # Base case: If the dimension has no parent, it is the root dimension
    if dimension.parent_id is None:
        return dimension
    else:
        # Recursive case: Traverse up the hierarchy
        return find_root_dimension(dimension.parent)


def delete_cache_key_of_newly_added_dimension(root_id):
    cache_key = f"dimension_hierarchy_{root_id}"
    cache.delete(cache_key)
    print(f"Cache key {cache_key} deleted.")