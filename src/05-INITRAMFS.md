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

* dev, proc ve sys dizinlerini bağla

* Modülleri yükle (devd ile)

* Kurulu sistemi /proc/cmdline içerisindeki root=xxx parametresinden bul ve bağla

* Kendini ram üzerinden temizle

* Kurulu sisteme geçiş yap


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

