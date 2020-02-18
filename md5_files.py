import glob
import hashlib

filenames = glob.glob("C:\\logs\\*.*")

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(2 ** 20), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == "__main__":
    for filename in filenames:
        print(filename, md5(filename))
