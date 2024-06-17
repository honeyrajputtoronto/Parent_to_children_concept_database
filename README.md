
1. Explain what SQL queries your solution is making and why.

    In list_children(root_id), first query is of fetching the root dimension object for the given root_id. select_related('parent', 'company') is used to perform a 
    single join query to fetch related parent and company objects in one go. The second query retrieves all Dimension objects from the database. Again, 
    select_related('parent', 'company') is used to optimize fetching related parent and company objects.
    
    In list_heirarchy(root_id), first I fetch the company details based on the given root_id. The second query retrieves all Dimension objects associated with 
    the given company. The select_related('parent', 'company') is used to fetch related parent and company objects in one go.

2. Assume there are hundreds of dimensions and the hierarchy is loaded on every page load. What caching strategies would you suggest?
    - Hint: The answer here is not a SQL query using `RECURSIVE`.

    Caching can be done on the entire hierarchical structure as a serialized object in Json format (example). it provides a quick way to retrieve the whole hierarchy without needing 
    to traverse the database each time.
  
    Updating the entire cached tree for minor changes is inefficient. Fragment caching allows caching and invalidating specific
    parts of the hierarchy, making updates more manageable and efficient.
  
    To ensure that the cache remains up to date without affecting user response times, utilize background tasks to asynchronously update cache entries. This will maintain 
    a fresh cache without delaying user requests
