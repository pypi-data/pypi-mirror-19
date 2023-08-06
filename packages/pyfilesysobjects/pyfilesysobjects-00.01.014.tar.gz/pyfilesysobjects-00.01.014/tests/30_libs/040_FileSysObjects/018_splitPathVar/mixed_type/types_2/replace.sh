#A0="'file://///'+filesysobjects.FileSysObjects.normpathX('hostname/share/a/b/c')"
#A1="'SHARE','hostname', 'share', filesysobjects.FileSysObjects.normpathX('a/b/c')"


#SMB
# B0="'smb://'+filesysobjects.FileSysObjects.normpathX('hostname/share/a/b/c')"
# B1="'SMB','hostname', 'share', filesysobjects.FileSysObjects.normpathX('a/b/c')"

#CIFS
# B0="'cifs://'+filesysobjects.FileSysObjects.normpathX('hostname/share/a/b/c')"
# B1="'CIFS','hostname', 'share', filesysobjects.FileSysObjects.normpathX('a/b/c')"

#SHARE
# B0="'file://///'+filesysobjects.FileSysObjects.normpathX('hostname/share/a/b/c')"
# B1="'SHARE','hostname', 'share', filesysobjects.FileSysObjects.normpathX('a/b/c')"

#FILE_DRIVE
# B0="'file://'+'d:'+filesysobjects.FileSysObjects.normpathX('hostname/share/a/b/c')"
# B1="'LDSYS','', 'd:', filesysobjects.FileSysObjects.normpathX('hostname/share/a/b/c')"

#FILE_LFSYS
# B0="'file://'+filesysobjects.FileSysObjects.normpathX('/hostname/share/a/b/c')"
# B1="'LFSYS','', '', filesysobjects.FileSysObjects.normpathX('/hostname/share/a/b/c')"

#DRIVE_PATH
# B0="filesysobjects.FileSysObjects.normpathX('d:/hostname/share/a/b/c')"
# B1="'LDSYS','', 'd:', filesysobjects.FileSysObjects.normpathX('/hostname/share/a/b/c')"

#DRIVE_ROOT
A0="filesysobjects.FileSysObjects.normpathX('d:/hostname/share/a/b/c')"
A1="'LDSYS','', 'd:', filesysobjects.FileSysObjects.normpathX('/hostname/share/a/b/c')"
B0="filesysobjects.FileSysObjects.normpathX('d:/')"
B1="'LDSYS','', 'd:', filesysobjects.FileSysObjects.normpathX('/')"




find . -type f -name '*.py' -exec sed -i "s|$A0|$B0|g" {} \;
find . -type f -name '*.py' -exec sed -i "s|$A1|$B1|g" {} \;

#find . -type f -name '*.py' -exec sed -n "s|$A0|$B0|gp" {} \;
#find . -type f -name '*.py' -exec sed -n "s|$A1|$B1|gp" {} \;
