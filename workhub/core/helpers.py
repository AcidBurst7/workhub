def get_user_group(request):
    user_group = 'guest'
    for group in request.user.groups.all():
        user_group = group.name
    return user_group

def generate_numbers_list(raw_ids):
    try:
        id_list = [int(pk) for pk in raw_ids.split(',') if pk.strip().isdigit()]
    except ValueError:
        id_list = []
    return id_list

def get_status_job_order(order='asc'):
    status_order = '9, 8, 6, 3, 2, 1, 4, 7, 10, 11, 13, 14, 15'
    if order == 'desc':
        status_order = '15, 14, 13, 11, 10, 7, 4, 1, 2, 3, 6, 8, 9'
    return status_order