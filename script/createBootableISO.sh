apt-get install extlinux syslinux-common
apt-get install syslinux-utils syslinux-efi
docker ps | sed -n 2p | awk '{print $1}' | xargs -I {} docker commit {} initramfs
docker image save initramfs -o initramfs.tar
tar xf initramfs.tar
cat repositories
mkdir root
####
tar xf 95c20b5c9ef093a111e6ce206dc1696a12b2e897675ddcca4b696906bc6cb10e/layer.tar -C root
tar xf 906cb5487ad7ecda271f9cd1e6f4acf03245d91bb40d941e6ea9edb7989afd49/layer.tar -C root/
mkdir root/proc root/sys
cd root
echo "#!/bin/sh
 
 
mount -t proc none /proc
mount -t sysfs none /sys
 
 
cat <<!
 
Boot took $(cut -d' ' -f1 /proc/uptime) seconds
 
Welcome to your docker image based linux.
!
exec /bin/sh" > init
cd ..
chmod +x root/init
cd root/
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz
cd ..
git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git # This will take a while, go get some coffee.
cd linux
make allnoconfig
####
make menuconfig
####
make -j8
cp arch/x86_64/boot/bzImage ..
cd ..
ls -lh bzImage initramfs.cpio.gz
truncate -s100M bootable.iso
####
fdisk bootable.iso
####
START=$((512 * 2048))
SIZE="99M"
DEVICE=$(losetup -o $START --sizelimit $SIZE --show --find bootable.iso)
mkfs.fat -F 16 $DEVICE
apt-get update
syslinux -i $DEVICE
find / -name mbr.bin 2>/dev/null
dd bs=440 count=1 conv=notrunc if=/usr/lib/syslinux/mbr/mbr.bin of=bootable.iso
mkdir disk
sudo mount $DEVICE disk
sudo cp bzImage initramfs.cpio.gz disk
cd disk
echo "DEFAULT linux
LABEL linux
LINUX bzImage
append console=ttyS0
INITRD initramfs.cpio.gz" > syslinux.cfg
cd ..
sudo umount disk
losetup -d $DEVICE