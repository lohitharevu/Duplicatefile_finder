import streamlit as st
import os
import hashlib

def get_hash(file_path):
    h = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

st.title("Simple Duplicate File Finder")

folder = st.text_input("Enter folder path")

if st.button("Scan"):
    if not os.path.isdir(folder):
        st.error("Invalid folder path")
    else:
        hashes = {}
        duplicates = {}

        for root, _, files in os.walk(folder):
            for name in files:
                path = os.path.join(root, name)
                try:
                    file_hash = get_hash(path)
                    if file_hash in hashes:
                        duplicates.setdefault(file_hash, []).append(path)
                        duplicates[file_hash].append(hashes[file_hash])
                    else:
                        hashes[file_hash] = path
                except:
                    pass

        if duplicates:
            st.write("Duplicates found:")
            for files in duplicates.values():
                st.write(files)
        else:
            st.success("No duplicates found!")