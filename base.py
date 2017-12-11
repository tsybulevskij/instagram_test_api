import csv
import os.path

from InstagramAPI import InstagramAPI


class ParseRecordsFollowingUsers(InstagramAPI):

    def get_following_users(self):
        """
        Get user id and parse all following users extracting user names
        :return: list of users names
        """
        self.users = self.getTotalFollowings(self.username_id)
        user_names = [user['username'] for user in self.users]
        return user_names

    @staticmethod
    def write_to_csv(user_names):
        """
        Write user names to csv file
        """
        with open('instagram_users.csv', 'w', newline='') as csvfile:
            user_writer = csv.writer(csvfile, delimiter=' ', quotechar='|',
                                     quoting=csv.QUOTE_MINIMAL)
            for user in user_names:
                user_writer.writerow([user])

    def find_user_id(self, unfollow_usersnames):
        """
        find users ids by user_names
        :param unfollow_usersnames: list with usernames for unfollowing
        :return: list of user ids
        """
        unfollow_user_ids = []
        for user_info in self.users:
            if user_info['username'] in unfollow_usersnames:
                unfollow_user_ids.append(user_info['pk'])
        return unfollow_user_ids

    def unfollow_users(self, filename):
        """
        Get usernames from .csv file and unfollowing
        :param filename: csv file with usernames list
        """
        unfollow_usersnames = []

        if filename:
            if os.path.isfile(filename):
                with open(filename, newline='') as csvfile:
                    user_reader = csv.reader(csvfile,
                                             delimiter=' ',
                                             quotechar='|')
                    for user_name in user_reader:
                        unfollow_usersnames.append(user_name[0])
                unfollow_user_ids = self.find_user_id(unfollow_usersnames)
                for user_id in unfollow_user_ids:
                    self.unfollow(user_id)
            else:
                print('file for unfollow does not exist')


if __name__ == '__main__':
    username = input('enter username: ')
    password = input('enter password: ')
    unfollow_csv = input('enter file name for unfollow: ')
    api = ParseRecordsFollowingUsers(username=username, password=password)
    api.login()
    user_names = api.get_following_users()
    api.write_to_csv(user_names)
    api.unfollow_users(unfollow_csv)
