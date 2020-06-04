import json


class NetflixFinder:
    def __init__(self):
        with open("forensic_files.json") as f:
            self.data = json.load(f)

    def find_episode(self, title):
        for episode in self.data:
            if episode['title'] == title:
                if 'netflix_collection_number' in episode and 'netflix_episode_number' in episode:
                    return episode['netflix_collection_number'], episode['netflix_episode_number']
        return -1, -1  # Error if we can't find the netflix collection and episode
