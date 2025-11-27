import os
import json

class DataHandler:
    _dbPath = "./db/"

    def __init__(self):
        if not os.path.exists(self._dbPath):
            os.makedirs(self._dbPath)

    def addNewEntry(self, newId, newName):
        newEntry = {"id": newId, "name": newName}
        try:
            with open(self._dbPath + "{}.json".format(newId), "x", encoding="utf-8") as fp:
                json.dump(newEntry , fp, indent=4, ensure_ascii=False) 
        except FileExistsError:
            print("id:{} already exists".format(newId))
            raise

    def editEntry(self, id, newName): 
        try:
            data = self.getEntry(id) 
        except:
            print("failed to get data in editEntry")
            raise

        data["name"] = newName
        with open(self._dbPath + "{}.json".format(id), "w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)

    def getEntry(self, id):
        try:
            with open(self._dbPath + "{}.json".format(id), "r", encoding="utf-8") as fp:
                data = json.load(fp) 
        except FileNotFoundError:
            print("id:{} does not exists".format(id))
            raise
        return data