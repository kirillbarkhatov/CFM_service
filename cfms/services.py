def validate_category_type(category, type_):
    """
    Проверяет, что категория относится к выбранному типу.
    """

    if category and type_ and category.type_id != type_.id:
        return False
    return True


def validate_subcategory_category(subcategory, category):
    """
    Проверяет, что подкатегория относится к выбранной категории.
    """

    if subcategory and category and subcategory.category_id != category.id:
        return False
    return True
