import os
from datetime import datetime


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if request.user.groups.filter(name='manager').exists():
                request.session['manager_entry_time'] = entry_time
                self.write_to_file(request.user.username, request.user.groups, entry_time)
            elif request.user.groups.filter(name='user').exists():
                request.session['user_entry_time'] = entry_time
                self.write_to_file(request.user.username, request.user.groups, entry_time)


        response = self.get_response(request)

        if request.path == '/accounts/login/?next=/' and request.user.is_authenticated:
            if 'manager_entry_time' in request.session:
                entry_time = datetime.strptime(request.session['manager_entry_time'], '%Y-%m-%d %H:%M:%S')
                spend_time = datetime.now() - entry_time
                self.write_to_file(request.user.username, request.user.groups, spend_time)

            request.session.clear()

        return response


    def write_to_file(self, username, user_type, spent_time):
        file_path = os.path.join('games', 'tracking_time.txt')
        with open(file_path, 'a') as file:
            file.write(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - User: {username}, Type: {user_type}, Spent Time: {spent_time}\n")
