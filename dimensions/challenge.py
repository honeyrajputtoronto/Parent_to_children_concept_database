from .models import Company, Dimension


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
        children = parent_to_children.get(dimension.id, [])
        indentation = '\t' * level
        res = f"{indentation}{dimension.name}"
        result.append(res)
        if children:
            result.extend(traverse(children, parent_to_children, level + 1))
    return result


def list_children(root_id):
    try:

        root_dimension = Dimension.objects.select_related('parent','company').get(id=root_id)

        all_dimension = Dimension.objects.select_related('parent','company').all()

        parent_to_children = collect_parent_to_children(all_dimension)

        result = traverse(root_dimension, parent_to_children)
        return result

    except Dimension.DoesNotExist:
        print('Root Dimension does not exist. ')
        return None


def list_hierarchy(root_id):
    try:
        company = Company.objects.get(id=root_id)

        dimensions = Dimension.objects.filter(company=company).select_related('parent','company')

        parent_to_children = collect_parent_to_children(dimensions)

        top_level_dimensions = [dim for dim in dimensions if dim.parent_id== None]

        result = traverse(top_level_dimensions, parent_to_children)

        return result

    except company.DoesNotExist:
        print('COmpany does not exist')
        return None


