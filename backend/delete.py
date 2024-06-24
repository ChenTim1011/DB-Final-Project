import os

DATABASE = 'library.db'

# 
if os.path.exists(DATABASE):
    os.remove(DATABASE)
