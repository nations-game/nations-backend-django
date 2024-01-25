def validate_dict_types(dictionary: dict, type_list: list[tuple[str, object]]) -> bool:
    try:
        check = [isinstance(dictionary[puppy[0]], puppy[1]) for puppy in type_list]
    except KeyError:
        return False

    return all(check)