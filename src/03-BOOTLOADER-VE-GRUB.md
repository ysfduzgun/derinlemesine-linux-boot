# Önyükleyici (bootloader)
Bootloader (Önyükleyici), bilgisayar donanımı (BIOS/UEFI) başarıyla başlatıldıktan sonra kontrolü devralan ve işletim sisteminin çekirdeğini (kernel) belleğe yükleyerek çalıştırmakla görevli olan kritik bir yazılımdır.
Linux çekirdeğini, initramfs imajını  ve çekirdek parametrelerini yüklemek için kullanılır.
Bununla birlikte birden çok işletim sitemini duruma göre çalıştırmak için de kullanılabilir.

Dağıtımlar tarafından tercih edilen bazı önyükleyiciler: grub2, u-boot, systemd-boot, lilo, syslinux, rEFInd, EfiStub

## Grub2
GNU projesi altında geliştirilen linux dağıtımlarınca eç çok tercih edilen önyükleyicidir.
Gelişmiş yapılandırma desteği ve modüler yapısı ile oldukça esnek bir yapıya sahiptir.

### Kurulum
Grub linux dağıtımı üzerine paket olarak kurulduktan sonra hedef disk üzerine kurulmalıdır.
Bunun için `grub-install` komutu kullanılır.

UEFI sistemler için grub **/boot/efi/EFI/<distro>/grubx64.efi** içerisinde bulunur.
Buradan dağıtımın bulunduğu diskte bulunan **/boot/grub** dizinine gider ve geri kalanı oradan yüklenir.

Uefi olmayan eski tip (Legacy) sistemler için ise diskin MBR alanına yazılır.
MBR alanından çalışan grub dağıtımın bulunduğu diskteki **/boot/grub** dizinine gider ve geri kalanı oradan yüklenir.

**Not:** Grub imajını sistemden bağımsız hale getirmek için `grub-mkstandalone` komutunu kullanabilirsiniz.

### Yapılandırma
Grub yapılandırması **/etc/default/grub** dosyası içerisinde yapılır ve `grub-mkconfig -o /boot/grub/grub.cfg` komutu ile yapılandırma güncellenir.

Örneğin:

```
# gösterme süresini 3 saniye yapmak için
GRUB_TIMEOUT=3
# varsayılan parametreler
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
# console moduna almak için (gfx modunu kapatır)
GRUB_TERMINAL=console
# diğer sistemleri taramaması için
GRUB_DISABLE_OS_PROBER=true
```

**Not:** Grub teması için terminal modu grafik modda olmalı ve `GRUB_THEME=` yapılandırması ayarlanmış olmalı.
Grub önyükleyici olduğu için sınırlı kaynağa sahiptir ve bazı durumlarda tema ayarlamak yavaşlığa sebep olabilir.
Bunu önlemek için **console** modunu kullanabilirsiniz.

### Grub konsolu
Grub ekranında `c` tuşuna basıldığında veya yapılandırma olmadığı durumda konsol ekranı açılır.

```
grub rescue>
```

Bu ekranda komut girerek sistemi elle başlatabilirsiniz.

```
set root=(hd0,msdos1)
linux /boot/vmlinuz-6.12.113+deb13-amd64 root=/dev/sda1 ro quiet splash
initrd /boot/initrd.img-6.12.113+deb13-amd64
boot
```

## EfiStub
EFISTUB (EFI Boot Stub), Linux çekirdeğinin (kernel) GRUB, rEFInd veya systemd-boot gibi harici bir önyükleyiciye (bootloader) ihtiyaç duymadan directly/doğrudan UEFI donanım yazılımı tarafından başlatılabilmesini sağlayan yerleşik bir özelliktir.
Modern Linux çekirdekleri, kendilerini UEFI donanım yazılımına sanki standart birer *.efi uygulamasıymış gibi gösterecek şekilde derlenirler.
Bilgisayarınız açıldığında anakartın UEFI arayüzü doğrudan Linux çekirdeğini okur ve sistemi başlatır.

### Kurulum
EFISTUB'ı kullanabilmek çekirdek imajının (vmlinuz) ve initramfs imajının ESP bölümünde bulunması gerekir.
```sh
cp /boot/vmlinuz-6.12.113+deb13-amd64 /boot/efi/vmlinuz-linux
cp /boot/initrd.img-6.12.113+deb13-amd64 /boot/efi/initramfs-linux.img
```

Ardından `efibootmgr` aracı ile Efi girdisi oluşturalım
```sh
efibootmgr --create \
   --disk /dev/sda --part 1 \
   --label "Linux EFISTUB" \
   --loader /vmlinuz-linux \
   --unicode 'root=UUID=6295c001-c4d7-4e07-acd9-7e6806a8594c ro initrd=\initramfs-linux.img quiet splash'
```

* **Not:** initramfs imajının konumu belirtilirken dizin ayracı olarak **\\** işareti kullanılır.

* **Not:** çekirdek güncellendiğinde initramfs imajı ve çekirdek imajını bulunduğu konuma elle tekrar kopyalamanız gerekir.

