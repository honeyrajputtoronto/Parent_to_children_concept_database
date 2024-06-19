# Define the dimensions data
dimensions = [
    {"model": "dimensions.dimension", "pk": 1, "fields": {
        "company": 1, "parent": None, "name": "Account", "has_children": True
        }
     },
    {"model": "dimensions.dimension", "pk": 2, "fields":
        {"company": 1, "parent": 1, "name": "Income Statement", "has_children": True
         }
        },
    {"model": "dimensions.dimension", "pk": 3, "fields":
        {"company": 1, "parent": 2, "name": "Revenue", "has_children": True
         }
        },
    {"model": "dimensions.dimension", "pk": 4, "fields":
        {"company": 1, "parent": 3, "name": "Product Revenue", "has_children": False
         }
        },
    {"model": "dimensions.dimension", "pk": 5, "fields": {"company": 1, "parent": 3, "name": "Services Revenue", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 6, "fields": {"company": 1, "parent": 2, "name": "Expense", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 7, "fields": {"company": 1, "parent": 2, "name": "Net Income", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 8, "fields": {"company": 1, "parent": 1, "name": "Balance Sheet", "has_children": True}},
    {"model": "dimensions.dimension", "pk": 9, "fields": {"company": 1, "parent": 8, "name": "Assets", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 10, "fields": {"company": 1, "parent": 8, "name": "Liabilities", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 11, "fields": {"company": 1, "parent": 8, "name": "Equity", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 12, "fields": {"company": 1, "parent": None, "name": "Scenario", "has_children": True}},
    {"model": "dimensions.dimension", "pk": 13, "fields": {"company": 1, "parent": 12, "name": "Actuals", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 14, "fields": {"company": 1, "parent": 12, "name": "Budget", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 15, "fields": {"company": 1, "parent": None, "name": "Department", "has_children": True}},
    {"model": "dimensions.dimension", "pk": 16, "fields": {"company": 1, "parent": 15, "name": "All Departments", "has_children":True}},
    {"model": "dimensions.dimension", "pk": 17, "fields": {"company": 1, "parent": 16, "name": "Marketing", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 18, "fields": {"company": 1, "parent": 16, "name": "Product", "has_children": True}},
    {"model": "dimensions.dimension", "pk": 19, "fields": {"company": 1, "parent": 18, "name": "Engineering", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 20, "fields": {"company": 1, "parent": 18, "name": "Design", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 21, "fields": {"company": 1, "parent": 16, "name": "General & Administrative", "has_children": True}},
    {"model": "dimensions.dimension", "pk": 22, "fields": {"company": 1, "parent": 21, "name": "Operations", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 23, "fields": {"company": 1, "parent": 21, "name": "Human Resources", "has_children": False}},
    {"model": "dimensions.dimension", "pk": 24, "fields": {"company": 1, "parent": 21, "name": "Finance & Accounting", "has_children": False}}
]

def find_related_dimensions(dimensions, root_pk):
    parent_to_children = {}
    pk_to_dimension = {}

    for dimension in dimensions:
        pk = dimension["pk"]
        parent = dimension["fields"]["parent"]
        if parent not in parent_to_children:
            parent_to_children[parent] = []
        parent_to_children[parent].append(pk)
        pk_to_dimension[pk] = dimension

    def traverse(parent_pk):
        related = [pk_to_dimension[parent_pk]]
        if parent_pk in parent_to_children:
            for child_pk in parent_to_children[parent_pk]:
                related.extend(traverse(child_pk))
        return related

    return traverse(root_pk)

root_pk = 1
related_dimensions = find_related_dimensions(dimensions, root_pk)

for dimension in related_dimensions:
    print(dimension)


parent_to_children.....
{None: [
    <Dimension: id: 1, Company: Sample Co, Parent: None, Name: Account, Has Children: True>,
    <Dimension: id: 15, Company: Sample Co, Parent: None, Name: Department, Has Children: True>,
    <Dimension: id: 12, Company: Sample Co, Parent: None, Name: Scenario, Has Children: True>
    ],
 12: [
     <Dimension: id: 13, Company: Sample Co, Parent: Scenario, Name: Actuals, Has Children: False>,
     <Dimension: id: 14, Company: Sample Co, Parent: Scenario, Name: Budget, Has Children: False>
     ],
 15: [
     <Dimension: id: 16, Company: Sample Co, Parent: Department, Name: All Departments, Has Children: True>
      ],
 8: [
     <Dimension: id: 9, Company: Sample Co, Parent: Balance Sheet, Name: Assets, Has Children: False>, <Dimension: id: 11, Company: Sample Co, Parent: Balance Sheet, Name: Equity, Has Children: False>, <Dimension: id: 10, Company: Sample Co, Parent: Balance Sheet, Name: Liabilities, Has Children: False>], 1: [<Dimension: id: 8, Company: Sample Co, Parent: Account, Name: Balance Sheet, Has Children: True>, <Dimension: id: 2, Company: Sample Co, Parent: Account, Name: Income Statement, Has Children: True>], 18: [<Dimension: id: 20, Company: Sample Co, Parent: Product, Name: Design, Has Children: False>, <Dimension: id: 19, Company: Sample Co, Parent: Product, Name: Engineering, Has Children: False>], 2: [<Dimension: id: 6, Company: Sample Co, Parent: Income Statement, Name: Expense, Has Children: False>, <Dimension: id: 7, Company: Sample Co, Parent: Income Statement, Name: Net Income, Has Children: False>, <Dimension: id: 3, Company: Sample Co, Parent: Income Statement, Name: Revenue, Has Children: True>], 21: [<Dimension: id: 24, Company: Sample Co, Parent: General & Administrative, Name: Finance & Accounting, Has Children: False>, <Dimension: id: 23, Company: Sample Co, Parent: General & Administrative, Name: Human Resources, Has Children: False>, <Dimension: id: 22, Company: Sample Co, Parent: General & Administrative, Name: Operations, Has Children: False>], 16: [<Dimension: id: 21, Company: Sample Co, Parent: All Departments, Name: General & Administrative, Has Children: True>, <Dimension: id: 17, Company: Sample Co, Parent: All Departments, Name: Marketing, Has Children: False>, <Dimension: id: 18, Company: Sample Co, Parent: All Departments, Name: Product, Has Children: True>], 3: [<Dimension: id: 4, Company: Sample Co, Parent: Revenue, Name: Product Revenue, Has Children: False>, <Dimension: id: 5, Company: Sample Co, Parent: Revenue, Name: Services Revenue, Has Children: False>]}


top_level_dimensions [
    <Dimension: id: 1, Company: Sample Co, Parent: None, Name: Account, Has Children: True>,
    <Dimension: id: 15, Company: Sample Co, Parent: None, Name: Department, Has Children: True>,
    <Dimension: id: 12, Company: Sample Co, Parent: None, Name: Scenario, Has Children: True>]