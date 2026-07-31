import os


class PersonaManager:

    def __init__(self, folder="personas"):
        self.folder = folder

    def load(self):
        personas = {}

        if not os.path.isdir(self.folder):
            return personas

        for file in os.listdir(self.folder):
            if file.endswith(".md"):
                path = os.path.join(self.folder, file)

                with open(path, "r", encoding="utf-8") as f:
                    personas[file[:-3]] = f.read()

        return personas
