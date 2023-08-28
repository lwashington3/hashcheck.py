from os.path import join, isfile
from os import getcwd, chdir
from sys import argv
from hashlib import md5, sha1, sha256
from tabulate import tabulate


class HashCheck(object):
	BUF_SIZE = 65536

	def __init__(self, check_file, hash_key):
		if not isfile(check_file):
			raise FileNotFoundError(f"{check_file} does not exist. Please try again.")
		self.hash_key = hash_key
		self.script_path = getcwd()
		# Reads in 64KB chunks
		self._methods = ({"md5": md5(), "sha1": sha1(), "sha256": sha256()})
		self.hash_generator(check_file)

	def __repr__(self):
		return self.validate()

	def hash_generator(self, file_name):
		"""self.check_file = self.check_file.replace("\\", "/")
		drive = str(self.check_file.split("/")[0])
		file_name = str(self.check_file.split("/")[-1])
		file_path = join(self.check_file.strip(file_name))
		if str(file_path.split("/")[0]) != drive:
			file_path = str(drive.strip(":") + file_path)
		if file_path != file_name:
			chdir(file_path)"""
		with open(file_name, "rb") as file:
			while True:
				data = file.read(self.BUF_SIZE)
				if not data:
					break
				for method in self._methods.values():
					method.update(data)

	def validate(self):
		lst = [(name, str(method.hexdigest())) for name,method in self._methods.items()]
		if self.hash_key is None:
			table = [[f"{other[0]}sum", other[1]] for other in lst]
			return tabulate(table, headers="firstrow", tablefmt="grid")

		for data in lst:
			name, hashed = data
			if hashed == self.hash_key:
				lst.remove(data)

				table = [["Validation:", "Hashes Match!"],
							["Key Given:", self.hash_key],
							[f"{name}sum", hashed]]

				for other in lst:
					table.append([f"{other[0]}sum", other[1]])

				return tabulate(table, headers="firstrow", tablefmt="grid")

		table = [["Validation:", "Hashes Don't Match!"],
				["Key Given:", self.hash_key]]
		for other in lst:
			table.append([f"{other[0]}sum", other[1]])
		return tabulate(table, headers="firstrow", tablefmt="grid")

	@classmethod
	def create(cls):
		check_file = input(r"Drag 'n Drop File Here: >> ").replace('"', "")
		hash_key = input(r"Enter Official hash-key here: >> ")
		return cls(check_file, hash_key)


if __name__ == "__main__":
	if len(argv) == 2:
		hash_check = HashCheck(argv[1], None)
	elif len(argv) == 3:
		hash_check = HashCheck(argv[1], argv[2])
	else:
		hash_check = HashCheck.create()
	print(hash_check)
