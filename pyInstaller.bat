"%USERPROFILE%\AppData\Local\Programs\Python\Python310\Scripts\pyinstaller.exe" ^
 ^
--add-data="fonts/FreeSansBold.ttf;./fonts" ^
--add-data="fonts/melted.ttf;./fonts" ^
 ^
--add-data="levels/level1/background.csv;./levels/level1" ^
--add-data="levels/level1/foreground.csv;./levels/level1" ^
--add-data="levels/level2/background.csv;./levels/level2" ^
--add-data="levels/level2/foreground.csv;./levels/level2" ^
--add-data="levels/level3/background.csv;./levels/level3" ^
--add-data="levels/level3/foreground.csv;./levels/level3" ^
--add-data="levels/level4/background.csv;./levels/level4" ^
--add-data="levels/level4/foreground.csv;./levels/level4" ^
--add-data="levels/level5/background.csv;./levels/level5" ^
--add-data="levels/level5/foreground.csv;./levels/level5" ^
--add-data="levels/level6/background.csv;./levels/level6" ^
--add-data="levels/level6/foreground.csv;./levels/level6" ^
--add-data="levels/level7/background.csv;./levels/level7" ^
--add-data="levels/level7/foreground.csv;./levels/level7" ^
--add-data="levels/level8/background.csv;./levels/level8" ^
--add-data="levels/level8/foreground.csv;./levels/level8" ^
 ^
--add-data="music/boss.mp3;./music" ^
--add-data="music/main.mp3;./music" ^
--add-data="music/level.mp3;./music" ^
--add-data="music/jingle.mp3;./music" ^
--add-data="music/credits.mp3;./music" ^
--add-data="music/timeOver.mp3;./music" ^
 ^
--add-data="res/animations/monster.png;./res/animations" ^
--add-data="res/animations/playerLmg.png;./res/animations" ^
--add-data="res/animations/playerPistol.png;./res/animations" ^
--add-data="res/animations/playerRifle.png;./res/animations" ^
--add-data="res/animations/playerSniper.png;./res/animations" ^
--add-data="res/animations/playerUnarmed.png;./res/animations" ^
--add-data="res/animations/zombie.png;./res/animations" ^
--add-data="res/collectables/ammo.png;./res/collectables" ^
--add-data="res/collectables/ammoBig.png;./res/collectables" ^
--add-data="res/collectables/crowbar.png;./res/collectables" ^
--add-data="res/collectables/empty.png;./res/collectables" ^
--add-data="res/collectables/lmg.png;./res/collectables" ^
--add-data="res/collectables/pickleBlood.png;./res/collectables" ^
--add-data="res/collectables/pickleChest.png;./res/collectables" ^
--add-data="res/collectables/pickleScreen.png;./res/collectables" ^
--add-data="res/collectables/pickleWall.png;./res/collectables" ^
--add-data="res/collectables/pickleWire.png;./res/collectables" ^
--add-data="res/collectables/revolver.png;./res/collectables" ^
--add-data="res/collectables/rifle.png;./res/collectables" ^
--add-data="res/collectables/sniper.png;./res/collectables" ^
--add-data="res/icon/icon.png;./res/icon" ^
--add-data="res/other/ammoUI.png;./res/other" ^
--add-data="res/other/bullet.png;./res/other" ^
--add-data="res/other/pickleBoy.png;./res/other" ^
--add-data="res/Tilesheet.png;./res" ^
 ^
--add-data="sounds/ammoPickup.mp3;./sounds" ^
--add-data="sounds/emptyGun.mp3;./sounds" ^
--add-data="sounds/gunPickup.mp3;./sounds" ^
--add-data="sounds/gunshot.mp3;./sounds" ^
--add-data="sounds/levelComplete.mp3;./sounds" ^
--add-data="sounds/meatDeath1.mp3;./sounds" ^
--add-data="sounds/meatDeath2.mp3;./sounds" ^
--add-data="sounds/meatSlap1.mp3;./sounds" ^
--add-data="sounds/meatSlap2.mp3;./sounds" ^
--add-data="sounds/meatSlap3.mp3;./sounds" ^
--add-data="sounds/secret.mp3;./sounds" ^
--add-data="sounds/swing.mp3;./sounds" ^
--add-data="sounds/playerDeath.mp3;./sounds" ^
 ^
--name "Transgenesis" ^
--icon "res/icon/icon.ico" ^
--noconfirm ^
--windowed ^
--onefile ^
--clean ^
scripts/main.py

rmdir /s /q "./build"
del "./Transgenesis.spec"