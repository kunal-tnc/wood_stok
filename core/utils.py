def group_by_combination(finished_log, seen_combinations):
    # Dictionary to store products for each unique combination
    products_by_combination = {}

    # Iterate over each combination
    for combination in seen_combinations:
        width, thickness = combination

        # Initialize an empty list for the combination
        products_by_combination[combination] = []

        # Iterate over each finished log
        for log in finished_log:
            # Check if the log matches the current combination
            if log.width == width and log.thickness == thickness:
                # Append the log to the corresponding combination
                products_by_combination[combination].append({
                    "id": log.id,
                    "length": log.length,
                    "width": log.width,
                    "thickness": log.thickness
                })

    return products_by_combination
