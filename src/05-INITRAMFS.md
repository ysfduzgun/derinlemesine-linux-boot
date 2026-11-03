# Initramfs
Initramfs aslında mini bir sisteme benzetilebilir.
Bu sistemin görevi gerekli sürücüleri (disk, dosya sistemi gibi) yükleyip ardından asıl kurulu olan sistemin bulunduğu diski bağlamaktır.

## Initramfs iç yapısı
initramfs dosyası özünde sıkıştırılmış bir cpio arşividir.
Bu arşivin içerisinde mini sistemimiz yer alır.

Mini sistemin içerisinde busybox, devd ve gereken diğer isteğe bağlı araçlar yer alır.
**/init** veya **/linuxrc** dosyası initramfs içerisinde asıl çalıştırılan kısımdır.

### busybox
Busybox yardımı ile temel komutlar kullanılabilir hale gelir.
Düşük boyutlu olması ve tek bir dosya olması initramfs için avantaj sağlar.
init dosyası genellikle busybox ile çalıştırılır.

### devd
Modüllerin tanımlanması ve gerekli olanlarının otomatik olarak yüklenmesini sağlar.

* systemd-udev: systemd tarafından sağlanan devd sistemidir.
Systemd içeren dağıtımlarda varsayılan olarak kullanılır.

* eudev: systemd-udev çatalıdır ve systemd olmadan çalıştırılabilir.
systemd-udev ile benzer yapıya sahiptir.

* busybox mdev: busybox içerisinde dahili gelir. eudev / systemd-udev kadar kapsamlı özelliklere sahip değildir.

Initramfs içerisinde devd aşağıdaki gibi çalıştırılır.
```sh
# systemd-udev / eudev için
/lib/systemd/systemd-udevd & # systemd-udev
/sbin/udevd & # eudev
udevadm trigger --action=add # donanım sürücüleri yüklemek için
udevadm settle # işlemin bitmesini beklemek için
udevadm control --exit # daemonu kapatmak için
# mdev için
/bin/busybox mdev -s
```

Bununla birlikte aşağıdaki gibi elle modüller yüklenebilir:
```sh
for file in /sys/bus/*/devices/*/uevent; do
    modalias=$(grep '^MODALIAS=' "$file" | cut -d= -f2)
    if [ -n "$modalias" ]; then
        modprobe -ab "$modalias" 2>/dev/null
    fi
done
```

### init
Bu dosya ilk çalıştırılan dosyadır. Sırası ile şunları gerçekleştirir.

1. dev, proc ve sys dizinlerini bağla

2. Modülleri yükle (devd ile)

3. Kurulu sistemi /proc/cmdline içerisindeki root=xxx parametresinden bul ve bağla

4. Kendini ram üzerinden temizle

5. Kurulu sisteme geçiş yap


Basit bir init örneği aşağıdaki gibidir:

```sh
#!/bin/busybox sh

# proc dev sys bağla.
mount -t devtmpfs devtmpfs /dev
mount -t proc proc /proc
mount -t sysfs sysfs /sys

# modülleri yükle (örneğin systemd-udev ile)
/lib/systemd/systemd-udevd &
udevadm trigger --action=add
udevadm settle
udevadm control --exit

# Dosya sistemini bağla (sda1 olduğunu varsaydık)
mount -o ro /dev/sda1 /root

# Dizinlerin bağını çıkar
umount /dev
umount /proc
umount /sys

# Asıl sisteme geç
exec switch_root /root /sbin/init
```

#### /proc/cmdline okunması
Çekirdeğe verilen parametreler */proc/cmdline* içerisinde yer alır. Örneğin:
```
BOOT_IMAGE=/boot/vmlinuz-6.12.113+deb13-amd64 root=UUID=6295c001-c4d7-4e07-acd9-7e6806a8594c ro quiet splash
```

* `root=...` parametresi sistemin kurulu olduğu diski belirtir. disklerin konumu (/dev/sda2 gibi) değişebileceği için değişmeyen **UUID** değeri ile belirtilebilir. Initramfs sistemimiz bu UUID değerinden hangi bölüm olduğunu tespit edip açılışa o disk üzerinden devam etmelidir.

* Varsa diğer parametreler (örneğin btrfs için `subvol=@` gibi) dikkate alınarak veya sistemin açılış esnasında ayarlanan özel parametreler (örneğin canlı sistem için `boot=live` parametresi) kullanılabilir.

* `ro` parametresi diskin sadece okunabilir olarak bağlanması gerektiğini belirtir. Eğer bunun yerine `rw` kullanılırsa disk yazılabilir olarak bağlanmalıdır. Diğer disklerin bağlanması ve bağlanma durumu için asıl sistem açılış esnasında `/etc/fstab` dosyasına bakar. Bu sebeple initramfs yalnızca çalıştırılacak olan sistemin bulunduğu diski bağlar. (Örneğin ayrı bir ev dizini diski varsa bağlanmaz)

* `quiet` parametresi çekirdek tarafından dikkate alınan ve ekrana daha az detaylı çıktı basılmasını sağlar. Bu parametresi initramfs içerisinde çıktıların ne seviyede basılacağını belirlemek için de kullanabilirsiniz.

* `splash` parametresi varsa **plymouth** servisini başlatmak için kullanılır. Bu sayede açılış sırasında kullanıcı akan yazılar yerine açılış animasyonu görür.

## initramfs oluşturulması
Linux dağıtımlarında initramfs oluşturmak için çeşitli araçlardan faydalanılır. (Debian için initramfs-tools, alpine için mkinitfs, archlinux için mkinitcpio, fedora için dracut gibi)
Bu araçlar çekirdeğin açılış için gereken dosyalarını ve ihtiyaç duyulan komutları ve bağımlı olduğu kütüphaneleri initramfs imajı içerisine ekler.

Bir initramfs dosyasını açmak için:
```sh
# xz ile sıkıştırılmış olan bir initramfs imajı için
xzcat /boot/initrd.img-6.12.113+deb13-amd64 | cpio -idmv
```

Bir initramfs imajı oluşturmak için:
```sh
find . | cpio -H newc -o | xz -9 > ../inird.img
```

