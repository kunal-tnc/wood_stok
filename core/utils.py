def group_by_combination(finished_log, seen_combinations):
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
