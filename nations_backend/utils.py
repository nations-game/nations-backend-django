from django.http import JsonResponse

def validate_dict_types(dictionary: dict, type_list: list[tuple[str, object]]) -> bool:
    try:
        check = [isinstance(dictionary[puppy[0]], puppy[1]) for puppy in type_list]
    except KeyError:
        return False

    return all(check)

def build_success_response(details: str, status_code: int, safe: bool = True) -> JsonResponse:
    return JsonResponse({
        "status": "success",
        "details": details
    }, status=status_code)

def build_error_response(details: str, status_code: int, safe: bool = True) -> JsonResponse:
    return JsonResponse({
        "status": "error",
        "details": details
    }, status=status_code)