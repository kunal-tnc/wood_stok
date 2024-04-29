def group_by_combination(finished_log, seen_combinations):
    """
    Groups finished logs by width and thickness combinations.

    Parameters:
    - finished_log (QuerySet): Queryset of FinishedLog objects.
    - seen_combinations (list of tuples): List of tuples representing seen width and thickness combinations.

    Returns:
    - dict: Dictionary where keys are width and thickness combinations and values are lists of logs.
    """
    products_by_combination = {}

    for combination in seen_combinations:
        width, thickness = combination

        products_by_combination[combination] = []

        for log in finished_log:
            if log.width == width and log.thickness == thickness:
                products_by_combination[combination].append(
                    {
                        "id": log.id,
                        "length": log.length,
                        "width": log.width,
                        "thickness": log.thickness,
                    }
                )

    return products_by_combination
