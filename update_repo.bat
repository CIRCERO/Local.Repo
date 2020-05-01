git pull

python update_repo.py .rebuilds
python update-directory-structure.py

git add .
git commit -a -m "update repo"
git push

pause
