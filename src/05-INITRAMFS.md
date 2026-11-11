# Initramfs

Initramfs (Initial RAM Filesystem), Linux çekirdeğinin gerçek kök dosya sistemine (root filesystem) erişmeden önce kullandığı geçici bir kullanıcı alanı ortamıdır.

Çekirdek açılış sırasında initramfs arşivini bellekteki özel kök dosya sistemine (rootfs) açar ve burada bulunan `/init` programını PID 1 olarak çalıştırır.

Initramfs'in temel görevleri şunlardır:

- Kök dosya sistemine erişmek için gereken donanım sürücülerini yüklemek.
- Diskleri ve disk bölümlerini tespit etmek.
- Gerekliyse LUKS, LVM ve RAID gibi depolama katmanlarını etkinleştirmek.
- Kök dosya sistemini bulmak ve bağlamak.
- Kontrolü asıl sistemin init sürecine devretmek.

Bu nedenle initramfs, yalnızca birkaç komuttan oluşan bir başlangıç betiği değil; gerektiğinde ağ bağlantısı kurabilen, şifreli diskleri açabilen ve depolama birimlerini hazırlayabilen küçük bir kullanıcı alanı ortamıdır.

## Initramfs iç yapısı

Initramfs, temel olarak `newc` biçiminde oluşturulmuş bir CPIO arşividir. Arşiv gzip, xz, zstd, lz4 gibi farklı algoritmalarla sıkıştırılabilir.

Çekirdek, arşivi açarak içindeki dosyaları bellekteki rootfs üzerine yerleştirir. Ardından `/init` dosyasını çalıştırır.

Örnek bir initramfs dizin yapısı:

```text
/
├── init
├── bin/
│   ├── sh
│   ├── mount
│   └── busybox
├── sbin/
│   ├── modprobe
│   └── udevd
├── dev/
├── proc/
├── sys/
├── lib/
│   └── modules/
├── etc/
└── scripts/
```

Bu yapı örnektir. Gerçek initramfs içerisindeki dosyalar kullanılan dağıtıma ve oluşturma aracına göre değişir.

### BusyBox

BusyBox, birçok temel Linux komutunu tek bir çalıştırılabilir dosyada birleştiren bir araç paketidir.

Initramfs içerisinde tercih edilmesinin başlıca nedenleri:

- Küçük boyutlu olması.
- Tek bir çalıştırılabilir dosya üzerinden çok sayıda komut sunması.
- Shell ve temel sistem araçlarını sağlayabilmesi.
- Sınırlı bellek ve depolama kaynaklarında çalışabilmesi.

Örneğin BusyBox kullanıldığında `sh`, `mount`, `mkdir`, `ls`, `grep` gibi komutlar aynı ikili dosya üzerinden çalıştırılabilir.

BusyBox zorunlu değildir. Initramfs içerisinde Bash, klibc araçları, systemd bileşenleri veya başka kullanıcı alanı araçları da kullanılabilir.

### udev ve aygıt yönetimi

Linux'ta donanım aygıtlarının tespit edilmesi ve bunlara karşılık gelen aygıt düğümlerinin yönetilmesi için udev altyapısı kullanılır.

Örneğin sistem açılırken SATA, NVMe veya USB depolama aygıtları tespit edildiğinde çekirdek ilgili donanım olaylarını kullanıcı alanına iletir. udev bu olayları değerlendirerek gerekli işlemleri gerçekleştirir.

Initramfs içerisinde kullanılabilecek başlıca çözümler:

| Araç | Açıklama |
|---|---|
| systemd-udevd | systemd projesinin sunduğu udev aygıt yöneticisi. |
| eudev | systemd bağımlılığı olmadan kullanılabilen udev çatalı. |
| BusyBox mdev | BusyBox içerisinde bulunan, daha küçük ve sınırlı özelliklere sahip aygıt yöneticisi. |

udev, donanım olaylarını takip ederek gerekli kernel modüllerinin yüklenmesini ve aygıt düğümlerinin oluşturulmasını sağlar.

Örnek bir udev başlatma akışı:

```sh
# udev daemon başlatılır.
udevd &

# Mevcut aygıtlar için olaylar oluşturulur.
udevadm trigger --action=add

# Olayların işlenmesi beklenir.
udevadm settle
```

Buradaki `udevd` ve `udevadm` yolları dağıtıma göre değişebilir. Örneğin systemd-udev ve eudev farklı konumlarda bulunabilir. Ayrıca gerçek initramfs uygulamalarında udev'in başlatılması, olayların işlenmesi ve durdurulması dağıtımın kendi betikleriyle yönetilir.

BusyBox mdev kullanıldığında mevcut aygıtların taranması için:

```sh
busybox mdev -s
```

komutu kullanılabilir. Dinamik donanım olaylarının yönetimi için ayrıca mdev'in hotplug yapılandırması gerekir.

### Kernel modüllerinin yüklenmesi

Kök dosya sisteminin bulunduğu diske erişebilmek için gerekli donanım ve dosya sistemi sürücülerinin yüklenmiş olması gerekir.

Örneğin NVMe disk üzerinde bulunan bir kök dosya sistemine erişmek için NVMe sürücüsünün; ext4 dosya sistemi kullanılıyorsa ext4 sürücüsünün kullanılabilir olması gerekir.

Gerekli modüller initramfs oluşturulurken arşive eklenir. Açılış sırasında udev, donanım olaylarına göre uygun modüllerin yüklenmesine yardımcı olur.

Modüller elle de yüklenebilir:

```sh
modprobe nvme
modprobe ext4
```

Donanımın PCI veya USB gibi veri yollarında tanımlanması ve modüllerin doğru sırada yüklenmesi gerektiğinden, gerçek sistemlerde elle modül yüklemek yerine udev ve modprobe altyapısının kullanılması tercih edilir.

## init dosyası

Initramfs içerisindeki `/init`, çekirdek tarafından çalıştırılan ilk kullanıcı alanı programıdır. PID 1 olarak çalışır ve gerçek kök dosya sistemine geçişi gerçekleştirir.

Burada önemli bir ayrım vardır:

- `/init`: Modern initramfs mekanizmasında kullanılan başlangıç programıdır.
- `/linuxrc`: Eski initrd mekanizmasıyla ilişkili bir başlangıç programıdır. Modern initramfs akışının standart başlangıç dosyası değildir.

Initramfs içerisindeki `/init` genellikle bir shell betiği olabilir. Ancak bunun mutlaka BusyBox ile yazılması gerekmez; derlenmiş bir program da olabilir.

### init dosyasının görevleri

Genel olarak aşağıdaki işlemleri gerçekleştirir:

1. Gerekli sanal dosya sistemlerini bağlamak (`/dev`, `/proc`, `/sys`).
2. Donanım aygıtlarını tespit etmek ve gerekli modülleri yüklemek.
3. Çekirdek komut satırındaki `root=` parametresini okumak.
4. Gerekli depolama katmanlarını hazırlamak (LUKS, LVM, RAID vb.).
5. Gerçek kök dosya sistemini bulmak ve bağlamak.
6. Gerekli dosya sistemlerini ve çalışma ortamını yeni kök dizine hazırlamak.
7. `switch_root` veya benzeri bir mekanizmayla gerçek kök dosya sistemine geçmek.
8. Asıl init programını çalıştırmak.

### Basit init örneği

Aşağıdaki örnek, temel mantığı göstermek amacıyla hazırlanmıştır. Gerçek bir dağıtımın initramfs betiklerinin yerini tutmaz.

```sh
#!/bin/sh

# Gerekli sanal dosya sistemleri için dizinleri oluştur.
mkdir -p /dev /proc /sys /root

# Sanal dosya sistemlerini bağla.
mount -t devtmpfs devtmpfs /dev
mount -t proc proc /proc
mount -t sysfs sysfs /sys

# Gerekli modülleri yükle.
modprobe nvme
modprobe ext4

# Kernel komut satırından root parametresini al.
ROOT=$(sed -n 's/.*root=\([^ ]*\).*/\1/p' /proc/cmdline)

# Gerçek kök dosya sistemini bul ve bağla.
mount -o ro "$ROOT" /root

# Gerçek sisteme geç.
exec switch_root /root /sbin/init
```

Bu örnekte bazı önemli noktalar basitleştirilmiştir:

- `root=` değerinin UUID olması durumunda ilgili bölümün bulunması gerekir. Örneğin `findfs UUID=...` kullanılabilir.
- LUKS, LVM veya RAID varsa kök dosya sistemi doğrudan bağlanamayabilir. Önce ilgili katmanların etkinleştirilmesi gerekir.
- Dosya sisteminin bağlanabilmesi için gerekli sürücüler ve araçlar initramfs içerisinde bulunmalıdır.
- udev kullanılıyorsa aygıtların hazır hale gelmesi beklenmelidir.
- `/dev`, `/proc` ve `/sys` dizinleri geçiş sırasında gelişigüzel ayrılmamalıdır. Kullanılan `switch_root` uygulamasının bu bağları nasıl yönettiğine dikkat edilmelidir.
- `switch_root` komutu initramfs'in eski kök ortamından gerçek kök dosya sistemine geçişi gerçekleştirir. Eski initramfs ortamının temizlenmesi ve yeni init programının çalıştırılması bu işlemin parçasıdır.

## Kernel parametrelerinin okunması

Çekirdeğe verilen komut satırı parametreleri `/proc/cmdline` dosyasında bulunur.

Örnek:

```text
BOOT_IMAGE=/boot/vmlinuz-6.12.113+deb13-amd64 root=UUID=6295c001-c4d7-4e07-acd9-7e6806a8594c ro quiet splash
```

Initramfs bu parametreleri okuyarak açılış işlemlerini yapılandırır.

Özellikle `root=` parametresi gerçek kök dosya sisteminin bulunması için kullanılır.

Örneğin:

```text
root=UUID=6295c001-c4d7-4e07-acd9-7e6806a8594c
```

Bu değer, kök dosya sisteminin bulunduğu bölümün UUID değerini belirtir.

UUID kullanımı önemlidir. Çünkü `/dev/sda2` gibi aygıt isimleri donanım algılama sırasına göre değişebilir. UUID ise bölümün kimliğini belirlemek için kullanılır.

Initramfs, UUID değerini ilgili disk bölümüyle eşleştirerek doğru aygıtı bulmalıdır.

Diğer bazı parametreler de initramfs tarafından değerlendirilebilir:

| Parametre | Kullanım amacı |
|---|---|
| `root=` | Gerçek kök dosya sisteminin konumunu belirtir. |
| `rootfstype=` | Kök dosya sisteminin türünü belirtir. |
| `rootflags=` | Kök dosya sistemi bağlanırken kullanılacak ek seçenekleri belirtir. |
| `ro` | Kök dosya sisteminin başlangıçta salt okunur bağlanmasını ister. |
| `rw` | Kök dosya sisteminin yazılabilir bağlanmasını ister. |
| `quiet` | Çekirdeğin konsola yazdığı mesajları azaltır. |
| `splash` | Dağıtımın açılış animasyonu altyapısı tarafından değerlendirilebilir. |

Örneğin Btrfs kullanılan bir sistemde:

```text
root=UUID=... rootflags=subvol=@
```

parametreleriyle kök dosya sisteminin hangi alt birimden bağlanacağı belirtilebilir.

Canlı sistemlerde ise:

```text
boot=live
```

gibi dağıtıma özel parametreler kullanılabilir. Bunlar genel Linux kernel parametreleri değil, ilgili initramfs veya canlı sistem altyapısının yorumladığı parametrelerdir.

### Kök dosya sisteminin bağlanması

Initramfs'in temel görevlerinden biri gerçek kök dosya sistemini hazırlamaktır.

Örneğin sistemin kök dosya sistemi `/dev/sda2` üzerinde bulunuyorsa, initramfs bu bölümü geçici olarak kendi ortamındaki bir dizine bağlar.

```sh
mount -o ro /dev/sda2 /root
```

Buradaki `/root` dizini, initramfs ortamında gerçek sistemin kök dizininin bağlandığı geçici konumdur. Bu isim zorunlu değildir; başka bir dizin de kullanılabilir.

Kök dosya sisteminin başlangıçta salt okunur bağlanması yaygın bir yöntemdir. Böylece dosya sistemi denetimleri ve gerekli başlangıç işlemleri gerçekleştirildikten sonra sistemin normal açılış sürecinde yazılabilir olarak yeniden bağlanması mümkün olur.

Ayrıca initramfs genellikle yalnızca kök dosya sistemini hazırlar. Ayrı bir `/home`, `/var` veya başka bir bölüm varsa bunların bağlanması çoğunlukla asıl sistemin init sürecinde `/etc/fstab` ve ilgili servisler tarafından gerçekleştirilir. Ancak özel yapılandırmalarda bu işlemler initramfs aşamasında da yapılabilir.

## switch_root ve gerçek sisteme geçiş

Kök dosya sistemi başarıyla bağlandıktan sonra initramfs ortamından çıkılarak gerçek sistemin kök dizinine geçilir.

Bu işlem için yaygın olarak `switch_root` kullanılır.

Örnek:

```sh
exec switch_root /root /sbin/init
```

Burada:

- `/root`: Gerçek kök dosya sisteminin bağlandığı dizindir.
- `/sbin/init`: Yeni kök dosya sisteminde çalıştırılacak init programıdır.
- `exec`: Mevcut initramfs başlangıç sürecinin yerini yeni programın almasını sağlar.

Bu işlem sırasında initramfs'in geçici kök ortamı devreden çıkarılır ve sistemin geri kalan açılış süreci gerçek kök dosya sisteminden devam eder.

`switch_root`, `pivot_root` ile aynı sistem çağrısı değildir. İkisi de kök dosya sistemi geçişiyle ilişkili olsa da çalışma biçimleri farklıdır. Initramfs rootfs özel bir yapıya sahip olduğundan geçişte genellikle `switch_root` veya benzeri yardımcı araçlar tercih edilir.

## Initramfs oluşturulması

Linux dağıtımları initramfs imajlarını hazırlamak için farklı araçlar kullanır.

| Dağıtım | Araç |
|---|---|
| Debian | initramfs-tools |
| Ubuntu | initramfs-tools |
| Arch Linux | mkinitcpio |
| Fedora | dracut |
| RHEL | dracut |
| Alpine Linux | mkinitfs |

Bu araçlar, ilgili çekirdek sürümü için gerekli modülleri, çalıştırılabilir dosyaları, kütüphaneleri, yapılandırmaları ve başlangıç betiklerini belirleyerek initramfs arşivini oluşturur.

İmajın içeriği kullanılan aracın yapılandırmasına göre değişebilir. Örneğin yalnızca mevcut donanım için gerekli modülleri içeren küçük bir imaj veya farklı donanımlarda da kullanılabilecek daha genel bir imaj hazırlanabilir.

### Initramfs içeriğini görüntüleme

Debian tabanlı sistemlerde:

```sh
lsinitramfs /boot/initrd.img-$(uname -r)
```

Arşivin içeriğini daha ayrıntılı incelemek veya çıkarmak için:

```sh
mkdir /tmp/initramfs
cd /tmp/initramfs

unmkinitramfs /boot/initrd.img-$(uname -r) .
```

`unmkinitramfs`, Debian'ın initramfs-tools paketinde sunulan bir araçtır. İmajın birden fazla bölüm veya arşiv içermesi gibi durumlarda doğrudan tek bir sıkıştırma komutuyla açmaya çalışmaktan daha uygundur.

### CPIO arşivini açma

Basit ve yalnızca xz ile sıkıştırılmış bir CPIO arşivi için:

```sh
xzcat initramfs.img | cpio -idmv
```

Burada:

- `-i`: Arşivden dosyaları çıkarır.
- `-d`: Gerekli dizinleri oluşturur.
- `-m`: Dosyaların zaman bilgilerini korur.
- `-v`: İşlemleri ayrıntılı gösterir.

Not: Her initramfs imajı doğrudan `xzcat` ile açılamaz. İmajın sıkıştırma algoritması ve yapısı bilinmelidir. Bazı imajlarda birden fazla arşiv veya erken yüklenen CPU microcode bölümü de bulunabilir.

### Basit bir initramfs oluşturma

Önceden hazırlanmış bir dizin ağacından CPIO arşivi oluşturmak için:

```sh
cd initramfs-root

find . -print0 | cpio --null -o -H newc | xz -9 > ../initramfs.img
```

Bu işlem, mevcut dizin yapısını `newc` biçiminde CPIO arşivine dönüştürür ve xz ile sıkıştırır.

Ancak bu komut tek başına önyüklenebilir, çalışan bir initramfs hazırlamaz. Arşivin içerisinde doğru dosyaların, çalıştırılabilir izinlerin, gerekli kütüphanelerin, kernel modüllerinin ve geçerli bir `/init` programının bulunması gerekir.

Ayrıca arşivdeki dosyaların sahiplik ve izin bilgilerinin doğru olması önemlidir. Gerçek sistemlerde initramfs oluşturma araçlarının tercih edilmesinin temel nedenlerinden biri de bu bağımlılıkları ve dosya izinlerini otomatik yönetmeleridir.

## Initramfs açılış akışı

Genel olarak initramfs aşaması şu şekilde ilerler:

```text
        Linux Kernel
              |
              v
   Initramfs arşivini aç
              |
              v
       /init çalıştırılır
              |
              v
  /dev, /proc ve /sys bağlanır
              |
              v
   Donanım ve sürücüler hazırlanır
              |
              v
  Kernel parametreleri okunur
              |
              v
  Gerekli depolama katmanları
       etkinleştirilir
              |
              v
   Gerçek root filesystem bulunur
              |
              v
    Gerçek root filesystem bağlanır
              |
              v
       switch_root
              |
              v
       Asıl init (PID 1)
              |
              v
     Normal sistem açılışı
```

Bu akış genel bir örnektir. Gerçek sıralama, dağıtımın kullandığı initramfs aracına ve sistemin depolama yapılandırmasına göre değişebilir.

## Sorun giderme

Initramfs aşamasında meydana gelen hatalar genellikle kök dosya sistemine erişilememesi veya gerekli sürücülerin yüklenememesiyle ilgilidir.

Sık karşılaşılan sorunlar:

| Sorun | Muhtemel neden |
|---|---|
| `Unable to find root device` | Diskin veya bölümün bulunamaması. |
| `UUID not found` | Yanlış UUID veya aygıtın henüz algılanmamış olması. |
| `VFS: Unable to mount root fs` | Kök dosya sisteminin bağlanamaması veya gerekli sürücünün bulunmaması. |
| Initramfs emergency shell | Açılış betiklerinin gerekli işlemleri tamamlayamaması. |
| LUKS açılmıyor | Şifreli disk katmanının açılamaması veya gerekli araçların bulunmaması. |

Debian sistemlerinde initramfs-tools tarafından sağlanan hata ayıklama parametreleriyle açılışın belirli aşamalarında shell ortamına düşülebilir.

Örneğin:

```text
break=premount
```

Bu sayede gerçek kök dosya sistemi bağlanmadan önce initramfs ortamında inceleme yapılabilir.

Initramfs shell içerisinde kullanılabilecek bazı komutlar:

```sh
cat /proc/cmdline
ls /dev
blkid
lsmod
dmesg
```

Bu komutlarla çekirdek parametreleri, algılanan diskler, bölüm UUID değerleri ve yüklenmiş modüller incelenebilir.
