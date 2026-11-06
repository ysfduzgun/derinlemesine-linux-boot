# Linux Önyükleme (Boot) Süreci

Bilgisayarın güç düğmesine basılmasıyla başlayan ve işletim sisteminin kullanıcı etkileşimine hazır hâle gelmesine kadar devam eden işlemler bütününe **önyükleme (boot) süreci** denir.

Linux sistemlerde bu süreç; donanımın hazırlanması, anakart firmware'inin önyükleme aygıtını belirlemesi, önyükleyicinin çekirdeği belleğe yüklemesi, çekirdeğin ilk kullanıcı alanını başlatması ve init sisteminin işletim sistemini kullanılabilir hâle getirmesi gibi aşamalardan oluşur.

Bu aşamalar genel olarak birbirini takip etse de bazı işlemler paralel yürütülebilir. Kullanılan donanıma, dağıtıma, önyükleyiciye, init sistemine ve disk yapılandırmasına göre ayrıntılar değişiklik gösterebilir.

## 1. POST ve Donanım Kontrolü (Power-On Self-Test)

Bilgisayarın güç düğmesine basıldığında işlemciye güç verilir ve işlemci, anakart firmware'inin (BIOS/UEFI) bulunduğu bellek alanındaki başlangıç kodunu çalıştırmaya başlar.

Bu aşamada POST (Power-On Self-Test) adı verilen başlangıç donanım kontrol işlemleri gerçekleştirilir.

POST işleminin temel amacı, bilgisayarın önyükleme yapabilmesi için gerekli temel donanım bileşenlerinin çalışır durumda olup olmadığını kontrol etmektir.

Bu aşamada gerçekleştirilebilen başlıca işlemler şunlardır:

- **İşlemci (CPU):** İşlemcinin başlangıç durumunun ve temel çalışma koşullarının kontrol edilmesi.
- **Bellek (RAM):** Belleğin algılanması ve başlangıç bellek kontrollerinin gerçekleştirilmesi.
- **Ekran birimi:** Görüntü çıkışının hazırlanması ve gerektiğinde ekran kartının başlatılması.
- **Depolama aygıtları:** SATA, NVMe ve diğer depolama denetleyicilerinin algılanması.
- **Temel çevre birimleri:** Klavye ve önyükleme için gerekli diğer donanım bileşenlerinin hazırlanması.

Donanım yapılandırmasına ve firmware üreticisine bağlı olarak POST sırasında bir hata tespit edilirse sistem açılışı durdurulabilir. Hata, anakartın sesli uyarıları, hata LED'leri veya ekranda gösterilen hata mesajları aracılığıyla kullanıcıya bildirilebilir.

POST işleminin başarıyla tamamlanması, bilgisayarın bütün donanımlarının kusursuz çalıştığı anlamına gelmez. Bu aşama yalnızca başlangıç için gerekli kontrolleri gerçekleştirir.

**Bu aşamanın sonucu:** Donanımın temel başlangıç kontrolleri tamamlanır ve kontrol, önyükleme işlemlerini yönetecek olan BIOS/UEFI firmware'ine geçer.

## 2. Anakart Yazılımı (BIOS/UEFI)

POST işleminin ardından BIOS veya UEFI firmware'i, sistemin önyükleme yapabilmesi için gerekli donanım bileşenlerini hazırlar ve hangi aygıttan başlatılacağını belirler.

BIOS (Basic Input/Output System), geleneksel bilgisayarlarda kullanılan firmware yaklaşımıdır. UEFI (Unified Extensible Firmware Interface) ise modern sistemlerde BIOS'un yerini alan, daha gelişmiş önyükleme ve donanım yönetimi olanakları sağlayan firmware standardıdır.

İki yaklaşım arasındaki temel farklardan biri, işletim sisteminin önyükleme koduna nasıl ulaşıldığıdır.

### Legacy BIOS (Geleneksel BIOS)

BIOS, yapılandırılmış önyükleme sırasına göre depolama aygıtını seçer ve seçilen diskin ilk sektöründeki MBR (Master Boot Record) önyükleme kodunu belleğe yükleyerek çalıştırır.

MBR tabanlı geleneksel önyükleme yapısında ilk aşama oldukça sınırlı bir kod alanına sahiptir. Bu nedenle GRUB gibi önyükleyiciler genellikle birden fazla aşamada yüklenir.

### UEFI (Unified Extensible Firmware Interface)

UEFI, BIOS'tan farklı olarak dosya sistemlerini tanıyabilir ve doğrudan EFI uygulamalarını çalıştırabilir.

Bu yapıda:

1. Firmware, NVRAM üzerinde kayıtlı önyükleme girdilerini (Boot Entries) kontrol eder.
2. Seçilen önyükleme girdisine ait disk ve bölüm belirlenir.
3. EFI System Partition (ESP) içerisindeki ilgili EFI uygulaması bulunur.
4. Önyükleyici veya doğrudan başlatılabilen bir işletim sistemi yükleyicisi çalıştırılır.

EFI System Partition genellikle FAT32 dosya sistemiyle biçimlendirilir ve içerisinde önyükleyicilere ait dosyalar bulunur.

Örnek EFI bölüm yapısı:

```text
/EFI
├── BOOT
│   └── BOOTX64.EFI
├── GRUB
│   └── grubx64.efi
└── systemd
    └── systemd-bootx64.efi
```

UEFI sistemlerde Secure Boot özelliği etkinse başlatılacak EFI uygulamalarının imzaları doğrulanabilir. Böylece önyükleme zincirinin güvenilirliği artırılabilir.

**Bu aşamanın sonucu:** Firmware, belirlenen önyükleme aygıtındaki önyükleyiciyi çalıştırır ve kontrolü işletim sisteminin başlatılmasını sağlayacak yazılıma devreder.

## 3. Önyükleyici (Bootloader)

Önyükleyici, BIOS/UEFI tarafından başlatılan ve işletim sisteminin çekirdeğini çalıştırılmaya hazırlayan yazılımdır.

Linux sistemlerde yaygın olarak kullanılan önyükleyiciler şunlardır:

- GRUB (GRand Unified Bootloader)
- systemd-boot
- Limine
- Syslinux

Önyükleyicinin temel görevi, işletim sisteminin çekirdek dosyasını ve gerekli başlangıç dosyalarını belleğe yükleyerek çekirdeğin çalıştırılmasını sağlamaktır.

GRUB gibi bazı önyükleyiciler kullanıcıya bir menü sunarak birden fazla işletim sistemi veya çekirdek sürümü arasından seçim yapılmasına imkân tanır.

Örneğin GRUB menüsünde şu seçenekler bulunabilir:

- Normal Linux çekirdeğiyle başlatma.
- Önceki bir çekirdek sürümüyle başlatma.
- Kurtarma modunda başlatma.
- Başka bir işletim sistemini başlatma.

Önyükleyici, seçilen yapılandırmaya göre aşağıdaki dosyaları belleğe yükleyebilir:

### Linux Kernel (vmlinuz)

Linux çekirdeğinin önyükleme için kullanılan sıkıştırılmış veya paketlenmiş çekirdek imajıdır. `vmlinuz` ismi yaygın bir dosya adlandırma geleneğidir; bütün Linux dağıtımlarında zorunlu bir dosya adı değildir.

Çekirdek imajı, donanım kaynaklarının yönetilmesi ve işletim sisteminin temel işlevlerinin yürütülmesinden sorumludur.

### Initramfs (Initial RAM File System)

Çekirdeğin asıl kök dosya sistemine erişebilmesi için ihtiyaç duyduğu erken kullanıcı alanı araçlarını ve dosyalarını içeren başlangıç dosya sistemidir.

### Kernel Parameters (Çekirdek Parametreleri)

Önyükleyici, çekirdeğe başlangıç sırasında kullanacağı parametreleri de iletir.

Örneğin:

```text
root=UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
ro
quiet
splash
```

Burada:

- `root=`: Asıl kök dosya sisteminin bulunduğu bölümü belirtir.
- `ro`: Kök dosya sisteminin başlangıçta salt okunur bağlanmasını ister.
- `quiet`: Açılış sırasında ekrana yazdırılan mesajları azaltır.
- `splash`: Destekleyen sistemlerde açılış ekranı gösterilmesini sağlar.

Önyükleyici, gerekli dosyaları belleğe yükledikten sonra çekirdeğin çalıştırılmasını sağlar.

**Bu aşamanın sonucu:** Linux çekirdeği ve varsa initramfs belleğe yüklenir. Kontrol çekirdeğe devredilir.

## 4. Çekirdek (Kernel) Başlangıcı

Önyükleyicinin kontrolü devretmesiyle Linux çekirdeğinin başlangıç süreci başlar.

Linux çekirdeği, işletim sisteminin donanım ile yazılım arasındaki temel yönetim katmanıdır. İşlemci, bellek, depolama aygıtları, ağ kartları ve diğer donanım bileşenleri üzerindeki işlemleri yönetir.

Çekirdeğin başlangıç aşamasında gerçekleştirilen başlıca işlemler şunlardır:

### 1. Çekirdeğin bellekte hazırlanması

Önyükleyici tarafından belleğe yüklenen çekirdek imajı, mimariye ve imaj biçimine bağlı olarak gerekli açma ve başlatma işlemlerinden geçirilir. x86 sistemlerde sıkıştırılmış çekirdek imajı kendi açılış kodu aracılığıyla açılarak çalışmaya hazırlanır.

### 2. Bellek yönetiminin başlatılması

Çekirdek, fiziksel ve sanal bellek yönetimini başlatır. Sistem belleğinin yönetilebilmesi için gerekli temel bellek yapılarını oluşturur.

### 3. İşlemci ve kesme mekanizmalarının hazırlanması

İşlemci çekirdekleri, zamanlayıcılar ve donanım kesmeleri için gerekli altyapı hazırlanır.

### 4. Donanım bileşenlerinin algılanması

Çekirdek, sistemdeki donanımları tanımaya ve gerekli sürücüleri yüklemeye başlar. Bu işlemler derleme sırasında çekirdeğe dahil edilmiş sürücülerle veya daha sonra yüklenen kernel modülleriyle gerçekleştirilebilir.

### 5. Temel dosya sisteminin oluşturulması

Çekirdek, başlangıç aşamasında kullanacağı geçici kök dosya sistemini hazırlar. Bu yapı `rootfs` olarak adlandırılır.

Çekirdeğin asıl kök dosya sistemine henüz erişemediği durumlarda initramfs içerisindeki araçlar devreye girerek bu erişimi mümkün hâle getirir.

Çekirdek başlangıç sürecinin sonunda ilk kullanıcı alanı sürecini çalıştırır. Initramfs kullanılıyorsa bu süreç genellikle initramfs içerisindeki `/init` programıdır.

**Bu aşamanın sonucu:** Çekirdek temel çalışma altyapısını hazırlar ve erken kullanıcı alanını başlatır.

## 5. initramfs ve Asıl Diskin Bağlanması

Initramfs (Initial RAM File System), Linux çekirdeğinin gerçek kök dosya sistemine erişebilmesi için gereken araçları ve yapılandırma dosyalarını içeren geçici bir dosya sistemidir.

Önyükleyici tarafından belleğe yüklenen initramfs imajı, çekirdek tarafından açılır ve geçici kök dosya sistemine yerleştirilir.

Bu ortam, sistemin gerçek kök dizini henüz bağlanmadan önce gerekli işlemlerin gerçekleştirilebilmesini sağlar.

Initramfs içerisinde bulunabilecek bileşenler şunlardır:

- Donanım sürücülerine ait kernel modülleri.
- Depolama aygıtlarını algılamak için gerekli araçlar.
- LVM ve RAID yönetim araçları.
- LUKS ve dm-crypt şifreleme araçları.
- Dosya sistemi yönetim araçları.
- udev kuralları ve aygıt yönetim bileşenleri.
- Başlangıç betikleri ve yapılandırma dosyaları.

### Asıl kök dosya sisteminin bulunması

Initramfs içerisindeki başlangıç programı, çekirdek parametrelerinde belirtilen kök dosya sisteminin konumunu belirler.

Örneğin kök dosya sistemi doğrudan bir NVMe bölümünde bulunabilir:

```text
/dev/nvme0n1p2
```

Ancak daha karmaşık disk yapılandırmalarında doğrudan bölümün bağlanması yeterli olmayabilir.

### Şifrelenmiş disklerin açılması

Kök dosya sistemi LUKS (Linux Unified Key Setup) ile şifrelenmişse, initramfs içerisindeki araçlar kullanıcıdan parola isteyebilir.

Bu parola, dm-crypt altyapısı aracılığıyla şifrelenmiş blok aygıtının açılması için kullanılır.

Örneğin:

```bash
cryptsetup luksOpen /dev/nvme0n1p2 cryptroot
```

Bu işlem başarılı olduğunda şifrelenmiş bölümün içeriğine erişilebilen yeni bir aygıt oluşturulur:

```text
/dev/mapper/cryptroot
```

### LVM ve RAID yapılandırmaları

Kök dosya sistemi LVM üzerinde bulunuyorsa mantıksal birimlerin etkinleştirilmesi gerekebilir.

Benzer şekilde yazılımsal RAID kullanılıyorsa RAID dizisinin bir araya getirilmesi gerekir.

Bu işlemlerin tamamı, gerçek kök dosya sistemi kullanılabilir hâle gelmeden önce gerçekleştirilebilir.

### Gerçek kök dosya sisteminin bağlanması

Gerekli aygıtlar hazırlandıktan sonra gerçek kök dosya sistemi geçici bir dizine bağlanır.

Örneğin:

```bash
mount /dev/mapper/cryptroot /sysroot
```

Buradaki `/sysroot` örnek bir bağlama noktasıdır. Kullanılan initramfs altyapısına göre `/new_root` gibi farklı dizinler de tercih edilebilir.

Initramfs yalnızca disk şifrelemesini çözmek için kullanılmaz. Karmaşık depolama yapılandırmalarını hazırlamak, dosya sistemini kontrol etmek ve hazırda bekletmeden dönüş gibi işlemleri gerçekleştirmek için de kullanılabilir.

**Bu aşamanın sonucu:** Gerçek kök dosya sistemi erişilebilir hâle getirilir ve sistemin asıl kullanıcı alanına geçiş için gerekli hazırlıklar tamamlanır.

## 6. Kök Dizine Geçiş (switch_root / pivot_root)

Initramfs ortamında gerekli işlemler tamamlandıktan sonra sistemin geçici kök dosya sisteminden gerçek kök dosya sistemine geçmesi gerekir.

Bu işleme *root filesystem switch* veya kök dosya sistemi geçişi denir.

Bu noktada iki önemli mekanizma karşımıza çıkar:

### pivot_root

Linux çekirdeği tarafından sağlanan `pivot_root()` sistem çağrısı, mevcut kök dosya sistemini başka bir kök dosya sistemine taşıyarak yeni kök dizinin kullanılmasını sağlar.

Eski kök dosya sistemi ayrı bir dizine taşınabilir ve daha sonra bağlantısı kesilebilir.

### switch_root

`switch_root`, özellikle initramfs ortamlarında kullanılan bir kullanıcı alanı aracıdır.

Yeni kök dosya sistemine geçiş yaparken eski initramfs içeriğinin temizlenmesine ve gerçek kök dosya sistemindeki init programının çalıştırılmasına yardımcı olur.

Örneğin:

```bash
switch_root /sysroot /sbin/init
```

Bu komut, yeni kök dosya sistemi olarak `/sysroot` dizinini kullanır ve oradaki `/sbin/init` programını başlatır.

Kullanılan initramfs altyapısına göre komutun uygulanışı ve bağlama noktaları değişebilir.

Önemli bir ayrıntı: Bu işlem sırasında geçici dosya sisteminin bütün içeriğinin mutlaka RAM'den fiziksel olarak silindiğini düşünmemek gerekir. Burada yapılan temel işlem, sistemin kök dosya sistemi referansının değiştirilmesi ve artık gerekmeyen geçici ortamın serbest bırakılmasıdır.

**Bu aşamanın sonucu:** Sistem, initramfs içerisindeki geçici ortamdan çıkarak gerçek Linux kök dosya sistemi üzerinde çalışmaya başlar.

## 7. İnit Sisteminin Devralması (PID 1)

Gerçek kök dosya sistemine geçiş tamamlandığında işletim sisteminin ana init sistemi çalışmaya başlar.

Linux sistemlerde kullanıcı alanında (userspace) başlatılan ilk süreç PID 1 numarasını alır. Bu süreç, sistemin geri kalanının başlatılmasından ve süreçlerin yönetilmesinden sorumludur.

Linux sistemlerde PID 1 görevini üstlenebilen başlıca init sistemleri şunlardır:

- **systemd:** Modern Linux dağıtımlarında yaygın olarak kullanılan, servisleri ve sistem kaynaklarını yöneten init sistemidir.
- **OpenRC:** Özellikle Gentoo ve Alpine Linux gibi dağıtımlarda kullanılan servis yönetim sistemidir.
- **SysVinit:** Geleneksel Unix/Linux başlangıç yaklaşımını kullanan init sistemidir.
- **runit:** Basitlik ve servislerin sürekli çalışır durumda tutulması üzerine tasarlanmış init sistemidir.

### systemd ile başlangıç süreci

systemd, sistem açılışını hedefler (targets), birimler (units) ve bağımlılıklar üzerinden yönetir.

Önyükleme sırasında sistemin ihtiyaç duyduğu temel birimler başlatılır. Bu birimler arasında:

- `local-fs.target`: Yerel dosya sistemlerinin bağlanması.
- `swap.target`: Takas alanlarının etkinleştirilmesi.
- `basic.target`: Temel sistem servislerinin hazırlanması.
- `network.target`: Ağ altyapısının başlangıç aşamasının tamamlanması.
- `multi-user.target`: Çok kullanıcılı, metin tabanlı çalışma ortamının hazırlanması.
- `graphical.target`: Grafiksel kullanıcı ortamının başlatılması.

Bu hedefler ve birimler arasındaki bağımlılıklar, hangi işlemin önce veya hangi işlemlerle eş zamanlı gerçekleştirileceğini belirler.

Örneğin ağ servisi, günlükleme servisi ve donanım yönetim servisleri uygun bağımlılıklar sağlandığında paralel olarak başlatılabilir.

### OpenRC ile başlangıç süreci

OpenRC, servisleri ve servis gruplarını (runlevels) kullanarak sistem başlangıcını yönetir.

Örneğin:

```bash
rc-status
```

Komutuyla mevcut servislerin ve çalışma seviyesinin durumu görüntülenebilir.

Bir servisi başlangıçta etkinleştirmek için:

```bash
rc-update add sshd default
```

Bu komut, SSH servisini varsayılan çalışma seviyesine ekler.

### Servislerin başlatılması

Init sistemi, yapılandırmasına göre aşağıdaki servisleri ve bileşenleri devreye alabilir:

- Sistem günlükleme servisleri.
- Ağ bağlantısı ve ağ yönetim servisleri.
- Donanım aygıtlarının yönetimi.
- Zaman eşitleme servisleri.
- SSH ve diğer uzak erişim servisleri.
- Ses altyapısı.
- Sistem güvenliği ve erişim denetimi bileşenleri.

Burada önemli olan, bütün servislerin tek tek ve kesin bir sırayla başlatılmadığıdır. Özellikle systemd gibi modern init sistemleri, servis bağımlılıklarını dikkate alarak uygun işlemleri paralel yürütebilir.

**Bu aşamanın sonucu:** Sistem servisleri başlatılır, gerekli çalışma ortamı hazırlanır ve kullanıcı oturumunun açılabilmesi için gerekli altyapı oluşturulur.

## 8. Kullanıcı Ekranı (GUI/TUI)

İnit sisteminin gerekli servisleri başlatmasının ardından sistem, yapılandırılmış çalışma seviyesine veya hedefine göre kullanıcı giriş ekranını hazırlar.

Linux sistemlerde kullanıcı etkileşimi temel olarak iki farklı şekilde gerçekleştirilebilir:

### TUI (Text User Interface)

Metin tabanlı kullanıcı arayüzüdür. Grafiksel masaüstü ortamı bulunmayan veya kullanılmayan sistemlerde kullanıcı, terminal üzerinden oturum açar.

Bu işlem genellikle `getty` ve `login` programları aracılığıyla gerçekleştirilir.

- `getty`: Sanal terminali hazırlar ve kullanıcı girişini bekler.
- `login`: Kullanıcının kimlik bilgilerini doğrular ve oturum açma işlemini gerçekleştirir.
- `shell`: Kullanıcı oturumu açıldıktan sonra komutların çalıştırılmasını sağlayan kabuk ortamını başlatır.

Örneğin Bash kabuğu kullanıldığında kullanıcı komut satırı üzerinden sistemle etkileşim kurabilir.

### GUI (Graphical User Interface)

Grafiksel kullanıcı arayüzüdür. Masaüstü ortamı kullanılacaksa init sistemi, yapılandırılmış görüntü yöneticisini (Display Manager) başlatır.

Yaygın görüntü yöneticileri şunlardır:

- **GDM:** GNOME masaüstü ortamında kullanılan görüntü yöneticisi.
- **SDDM:** KDE Plasma ile yaygın olarak kullanılan görüntü yöneticisi.
- **LightDM:** Farklı masaüstü ortamlarıyla kullanılabilen görüntü yöneticisi.

Görüntü yöneticisi, kullanıcıya grafiksel giriş ekranını sunar. Kullanıcı adı ve parola doğrulandıktan sonra ilgili masaüstü oturumu başlatılır.

Grafiksel oturumun hazırlanmasında ayrıca şu bileşenler görev alabilir:

- Grafik sunucusu veya görüntü protokolü altyapısı (Xorg / Wayland).
- Pencere yöneticisi veya masaüstü ortamı.
- Görüntü ve giriş aygıtı sürücüleri.
- Kullanıcı oturumuna ait başlangıç servisleri.

Kullanıcı başarılı şekilde oturum açtıktan sonra masaüstü veya terminal ortamı kullanıma hazır hâle gelir.

Bu noktada bilgisayarın önyükleme süreci tamamlanmış ve işletim sistemi normal çalışma durumuna geçmiş olur.

## 9. Linux Önyükleme Sürecinin Genel Akış Şeması

Linux önyükleme sürecinin genel akışı aşağıdaki şekilde özetlenebilir:

1. **POST ve donanım kontrolü:** CPU, RAM ve temel donanım hazırlığı.
2. **BIOS / UEFI:** Önyükleme aygıtının ve girdisinin belirlenmesi.
3. **Bootloader:** Kernel, initramfs ve kernel parametrelerinin yüklenmesi.
4. **Linux Kernel:** Çekirdek altyapısının başlatılması.
5. **initramfs:** Depolama, şifreleme ve gerçek kök dosya sistemine erişim.
6. **Root Switch:** Geçici kökten gerçek kök dosya sistemine geçiş.
7. **Init System (PID 1):** Servislerin ve sistem hedeflerinin başlatılması.
8. **Kullanıcı arayüzü:** TUI veya GUI üzerinden oturum açılması.

## 10. Konuyla İlgili Yararlı Linux Komutları

Önyükleme sürecini daha iyi anlamak ve sistem üzerinde inceleme yapmak için aşağıdaki komutlardan yararlanılabilir.

| Komut | Açıklama |
|---|---|
| `systemd-analyze` | Sistem açılış süresini gösterir. |
| `systemd-analyze blame` | Servislerin başlangıç sürelerini listeler. |
| `systemd-analyze critical-chain` | Kritik başlangıç bağımlılık zincirini gösterir. |
| `journalctl -b` | Mevcut açılışa ait günlükleri gösterir. |
| `dmesg` | Çekirdek mesajlarını görüntüler. |
| `lsblk -f` | Diskleri, bölümleri ve dosya sistemlerini listeler. |
| `findmnt /` | Gerçek kök dosya sisteminin bağlama bilgisini gösterir. |
| `cat /proc/cmdline` | Çekirdeğe iletilen başlangıç parametrelerini gösterir. |
| `ps -p 1 -f` | PID 1 sürecini ve çalıştırılan programı gösterir. |

**Not:** `systemd-analyze` komutları systemd kullanılan sistemlerde kullanılabilir. Diğer init sistemlerinde farklı araçlar tercih edilmelidir.

## Kaynakça ve İleri Okuma

1. [ArchWiki – Arch boot process](https://wiki.archlinux.org/title/Arch_boot_process)
2. [ArchWiki – Initramfs](https://wiki.archlinux.org/title/Initramfs)
3. [Gentoo Wiki – Bootloader](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Bootloader)
4. [Gentoo Wiki – Initramfs](https://wiki.gentoo.org/wiki/Initramfs)
5. [systemd – bootup(7)](https://man.archlinux.org/man/bootup.7.en)
6. [systemd – Initrd Interface](https://systemd.io/INITRD_INTERFACE/)

---

*Not: Bu dokümanda anlatılan süreç genel Linux önyükleme mimarisini açıklar. Dağıtım, donanım, önyükleyici ve init sistemi farklılıklarına bağlı olarak bazı aşamalar değişebilir.*