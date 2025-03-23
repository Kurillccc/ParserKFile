def filter_elements_by_subregion(elements, target_subregion):
    """Фильтрует элементы, оставляя только те, что принадлежат заданной подобласти."""
    return {
        element_id: data["nodes"]
        for element_id, data in elements.items()
        if data["subregion"] == target_subregion
    }
