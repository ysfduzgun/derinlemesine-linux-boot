# Önyükleyici (Bootloader)

Bootloader (Önyükleyici), bilgisayarın firmware'i (BIOS/UEFI) tarafından başlatılan ve işletim sisteminin çekirdeğini (kernel) çalıştırılmaya hazırlayan yazılımdır.

Önyükleyicinin temel görevi, Linux çekirdeğini, initramfs imajını ve çekirdek başlangıç parametrelerini belleğe yükleyerek kontrolü çekirdeğe devretmektir.

Bununla birlikte önyükleyiciler, birden fazla işletim sisteminin aynı bilgisayarda bulunması durumunda kullanıcıya seçim yapma imkânı da sunabilir. Böylece bilgisayar açılırken hangi işletim sisteminin veya çekirdek sürümünün başlatılacağı belirlenebilir.

Linux sistemlerde kullanılan önyükleyiciler, destekledikleri firmware mimarilerine, yapılandırma yöntemlerine ve sundukları özelliklere göre farklılık gösterir.

Yaygın olarak kullanılan bazı önyükleme çözümleri şunlardır:

- **GRUB2:** Gelişmiş yapılandırma, modüler mimari ve çoklu işletim sistemi desteği sunan önyükleyici.
- **systemd-boot:** UEFI sistemler için tasarlanmış, basit yapılandırma ve hızlı önyükleme odaklı önyükleyici.
- **U-Boot:** Özellikle gömülü sistemlerde ve ARM tabanlı cihazlarda kullanılan önyükleyici.
- **Syslinux:** BIOS ve bazı UEFI ortamlarında kullanılabilen hafif önyükleyici ailesi.
- **LILO:** Geleneksel Linux sistemlerinde kullanılan eski nesil önyükleyici.
- **rEFInd:** UEFI sistemlerde EFI uygulamalarını ve işletim sistemlerini algılayıp menü üzerinden başlatabilen önyükleme yöneticisi.
- **EFISTUB:** Linux çekirdeğinin UEFI tarafından doğrudan EFI uygulaması olarak başlatılmasını sağlayan özellik.

## 1. GRUB2 (GRand Unified Bootloader)

GRUB2, GNU projesi kapsamında geliştirilen ve Linux dağıtımlarında yaygın olarak kullanılan gelişmiş bir önyükleyicidir ([10], [12]).
Modüler mimarisi, geniş dosya sistemi desteği, farklı işletim sistemlerini algılayabilmesi ve esnek yapılandırma seçenekleri sayesinde çok çeşitli sistemlerde kullanılabilir.

GRUB2 hem geleneksel BIOS hem de UEFI tabanlı bilgisayarlarda çalışabilir.

GRUB'un öne çıkan özellikleri şunlardır:

- Birden fazla Linux çekirdeği arasından seçim yapabilme.
- Windows ve diğer işletim sistemlerini başlatabilme.
- Farklı dosya sistemlerinden çekirdek ve başlangıç dosyalarını okuyabilme.
- LUKS ve LVM gibi depolama yapılandırmalarını destekleyen modüllere sahip olma.
- Çekirdek parametrelerini değiştirebilme.
- Kurtarma ve hata ayıklama amacıyla komut satırı sunabilme.
- Tema ve grafiksel menü desteği.

### Kurulum

GRUB, Linux dağıtımlarında genellikle paket yöneticisi aracılığıyla kurulur ([2], [10], [12]).

Debian tabanlı sistemlerde:

```bash
sudo apt install grub2-common
```

BIOS sistemlerde kullanılan GRUB paketleri:

```bash
sudo apt install grub-pc
```

UEFI sistemlerde:

```bash
sudo apt install grub-efi-amd64
```

Paket isimleri dağıtıma ve mimariye göre değişebilir. Kurulum öncesinde sistemin BIOS veya UEFI modunda başlatıldığı kontrol edilmelidir.

#### BIOS (Legacy) Kurulumu

Geleneksel BIOS sistemlerde GRUB'un ilk aşama önyükleme kodu genellikle diskin MBR alanına yerleştirilir.

Örnek kurulum:

```bash
sudo grub-install /dev/sda
```

Burada `/dev/sda`, önyükleyicinin kurulacağı fiziksel diski ifade eder.

GRUB'un ilk aşama kodu MBR üzerinden çalıştırılır. Daha sonra gerekli GRUB bileşenleri disk üzerindeki diğer alanlardan yüklenir.

GPT bölümleme tablosu kullanan BIOS sistemlerde ise GRUB'un ikinci aşama bileşenlerini yerleştirebilmesi için genellikle BIOS Boot Partition adı verilen küçük bir bölüm gerekir.

#### UEFI Kurulumu

UEFI sistemlerde GRUB, EFI System Partition (ESP) içerisinde bir EFI uygulaması olarak bulunur.

Örneğin:

```text
/boot/efi/EFI/debian/grubx64.efi
```

Bu konum örnektir. Kullanılan dağıtıma ve kurulum seçeneklerine göre değişebilir.

Örnek kurulum:

```bash
sudo grub-install \
    --target=x86_64-efi \
    --efi-directory=/boot/efi \
    --bootloader-id=debian
```

Burada:

- `--target=x86_64-efi`: GRUB'un x86-64 UEFI sistemler için hazırlanmasını sağlar.
- `--efi-directory`: EFI System Partition'ın bağlandığı dizini belirtir.
- `--bootloader-id`: UEFI önyükleme menüsünde kullanılacak adı belirler.

Kurulum sonucunda EFI uygulaması ESP üzerine yerleştirilir ve uygun koşullarda UEFI NVRAM üzerinde yeni bir önyükleme girdisi oluşturulur.

GRUB'un EFI uygulaması ile yapılandırma dosyaları ve modülleri farklı konumlarda bulunabilir.

Örneğin:

```text
/boot/efi/EFI/debian/grubx64.efi
/boot/grub/grub.cfg
/boot/grub/x86_64-efi/
```

EFI uygulaması çalıştırıldığında gerekli modülleri ve yapılandırma dosyalarını bulup yükleyerek önyükleme menüsünü hazırlar.

**Not:** GRUB imajını mümkün olduğunca bağımsız hâle getirmek ve gerekli modülleri tek bir EFI uygulamasına dahil etmek için `grub-mkstandalone` kullanılabilir. Bu yöntem, standart kurulumdan farklı olarak özel bir imaj oluşturulmasını sağlar.

### Yapılandırma

GRUB'un temel yapılandırma seçenekleri Debian gibi birçok dağıtımda:

```text
/etc/default/grub
```

dosyası içerisinde düzenlenir.

Bu dosya doğrudan GRUB'un son yapılandırması değildir. `grub-mkconfig` tarafından kullanılan yapılandırma değişkenlerini içerir.

Yapılandırma değişikliklerinin uygulanabilmesi için GRUB yapılandırma dosyasının yeniden oluşturulması gerekir.

Debian ve benzeri sistemlerde:

```bash
sudo update-grub
```

Alternatif olarak:

```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

Örnek yapılandırma:

```bash
# GRUB menüsünün gösterilme süresi
GRUB_TIMEOUT=3

# Varsayılan çekirdek parametreleri
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"

# Metin tabanlı konsol kullanımı
GRUB_TERMINAL=console

# Diğer işletim sistemlerinin otomatik taranmasını kapatır
GRUB_DISABLE_OS_PROBER=true
```

Yapılandırma seçeneklerinin açıklamaları:

- `GRUB_TIMEOUT`: Önyükleme menüsünün kaç saniye görüntüleneceğini belirler.
- `GRUB_CMDLINE_LINUX_DEFAULT`: Normal önyükleme sırasında kullanılacak çekirdek parametrelerini tanımlar.
- `GRUB_TERMINAL`: GRUB menüsünün kullanılacağı terminal türünü belirler.
- `GRUB_DISABLE_OS_PROBER`: Diğer işletim sistemlerinin otomatik algılanmasını kontrol eder.

#### GRUB Temaları

GRUB, grafiksel menü ve tema desteğine sahiptir.

Tema kullanabilmek için grafiksel terminal yapılandırılmalı ve tema dosyasının konumu belirtilmelidir.

Örneğin:

```bash
GRUB_TERMINAL_OUTPUT=gfxterm
GRUB_THEME="/boot/grub/themes/mytheme/theme.txt"
```

Tema kullanımı GRUB'un grafiksel terminal altyapısına bağlıdır. Kullanılan çözünürlük, ekran kartı ve firmware desteğine göre görüntüleme farklılık gösterebilir.

Grafiksel menü kullanmak istenmediğinde:

```bash
GRUB_TERMINAL=console
```

yapılandırması tercih edilebilir.

Bu seçenek metin tabanlı bir menü sunar ve grafiksel tema kullanımını devre dışı bırakır.

GRUB'un açılış aşamasında sınırlı donanım ve grafik desteği bulunduğundan karmaşık temalar bazı sistemlerde görüntüleme sorunlarına veya gecikmelere neden olabilir.

### GRUB Konsolu ve Kurtarma

GRUB, önyükleme menüsünden komut satırı arayüzüne geçiş yapılmasına imkân tanır.

Menü ekranında `c` tuşuna basıldığında GRUB komut satırı açılır:

```text
grub>
```

GRUB'un bazı modülleri veya yapılandırma dosyaları yüklenemediğinde ise daha sınırlı bir kurtarma arayüzü açılabilir:

```text
grub rescue>
```

Bu iki konsol aynı değildir. `grub rescue>` ortamında kullanılabilen komutlar daha sınırlıdır.

Normal GRUB konsolunda sistemin elle başlatılması için örnek:

```bash
set root=(hd0,msdos1)
linux /boot/vmlinuz-6.12.113+deb13-amd64 root=/dev/sda1 ro quiet splash
initrd /boot/initrd.img-6.12.113+deb13-amd64
boot
```

Burada:

- `set root`: GRUB'un çekirdek dosyalarını arayacağı bölümü belirler.
- `linux`: Linux çekirdeğini ve başlangıç parametrelerini tanımlar.
- `initrd`: Initramfs imajının konumunu belirtir.
- `boot`: Başlatma işlemini gerçekleştirir.

`(hd0,msdos1)` ifadesi, ilk diskin MBR bölümleme yapısındaki ilk bölümünü ifade eder. GPT sistemlerde `(hd0,gpt1)` gibi bir ifade kullanılır.

Gerçek disk ve dosya yolları sistemin yapılandırmasına göre değişir.

GRUB konsolunda mevcut disk ve bölümleri görmek için:

```bash
ls
```

Belirli bir bölümün içeriğini görüntülemek için:

```bash
ls (hd0,msdos1)/
```

Bu komutlar, kurtarma sırasında doğru çekirdek ve initramfs dosyalarının bulunmasına yardımcı olur.

## 2. systemd-boot

systemd-boot, systemd projesinin bir parçası olarak geliştirilen, UEFI sistemler için tasarlanmış hafif bir önyükleyicidir ([13], [14]).
Önceki adıyla Gummiboot olarak bilinen bu yazılım, basit yapılandırma yapısı ve UEFI ile doğrudan çalışabilmesi sayesinde özellikle modern Linux sistemlerde tercih edilmektedir.

GRUB'dan farklı olarak BIOS (Legacy) sistemleri desteklemez. Yalnızca UEFI firmware üzerinde çalışır.

systemd-boot'un temel özellikleri şunlardır:

- UEFI tabanlı sistemlerde çalışır.
- EFI System Partition üzerindeki dosyaları kullanır.
- Basit metin tabanlı yapılandırma dosyalarına sahiptir.
- Birden fazla Linux çekirdeği arasında seçim yapılmasını sağlar.
- Windows Boot Manager gibi diğer EFI uygulamalarını menüye ekleyebilir.
- EFISTUB destekli Linux çekirdeklerini doğrudan başlatabilir.
- GRUB gibi karmaşık bir modül mimarisine sahip değildir.

systemd-boot, UEFI firmware'in EFI uygulamalarını çalıştırma yeteneğini kullanır. Kendi içerisinde gelişmiş bir dosya sistemi veya disk şifreleme çözme altyapısı bulunmaz. Bu nedenle önyükleme sırasında gerekli dosyaların EFI tarafından erişilebilir bir dosya sisteminde bulunması gerekir.

### Kurulum

systemd-boot kurulumu için öncelikle sistemin UEFI modunda başlatılmış olması gerekir.

EFI System Partition'ın bağlandığı dizin kontrol edilir:

```bash
findmnt /boot
findmnt /boot/efi
```

systemd-boot, systemd paketi içerisinde bulunur. Dağıtımın paketleme yöntemine göre ayrıca kurulum gerekebilir.

UEFI sistemlerde kurulum için:

```bash
sudo bootctl install
```

komutu kullanılabilir.

Bu komut systemd-boot EFI uygulamasını ESP içerisine kurar ve uygun koşullarda UEFI NVRAM üzerinde önyükleme girdisi oluşturur.

Kurulum sonrasında EFI System Partition içerisinde aşağıdakine benzer bir yapı bulunabilir:

```text
/boot
├── EFI
│   ├── systemd
│   │   └── systemd-bootx64.efi
│   └── BOOT
│       └── BOOTX64.EFI
├── loader
│   ├── loader.conf
│   └── entries
│       └── linux.conf
├── vmlinuz-linux
└── initramfs-linux.img
```

Dizin yapısı, ESP'nin hangi dizine bağlandığına ve dağıtımın yapılandırmasına göre değişebilir.

### Yapılandırma

systemd-boot yapılandırması temel olarak `loader` dizini içerisindeki dosyalar üzerinden gerçekleştirilir.

Ana yapılandırma dosyası:

```text
/boot/loader/loader.conf
```

Örnek yapılandırma:

```ini
default linux.conf
timeout 3
console-mode auto
editor no
```

Açıklamalar:

- `default`: Varsayılan olarak başlatılacak önyükleme girdisini belirtir.
- `timeout`: Önyükleme menüsünün görüntülenme süresini belirler.
- `console-mode`: Konsol çözünürlüğü ve görüntüleme modunu belirler.
- `editor`: Önyükleme sırasında çekirdek parametrelerinin düzenlenmesine izin verilip verilmeyeceğini belirler.

Linux çekirdeğine ait önyükleme girdileri ise:

```text
/boot/loader/entries/
```

dizini içerisinde tutulur.

Örneğin:

```text
/boot/loader/entries/linux.conf
```

Dosya içeriği:

```ini
title   Linux
linux   /vmlinuz-linux
initrd  /initramfs-linux.img
options root=UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx rw quiet splash
```

Burada:

- `title`: Önyükleme menüsünde görüntülenecek başlıktır.
- `linux`: Çekirdek imajının ESP içerisindeki konumunu belirtir.
- `initrd`: Initramfs imajının konumunu belirtir.
- `options`: Çekirdeğe iletilecek başlangıç parametrelerini içerir.

Birden fazla çekirdek sürümü kullanılacaksa her sürüm için ayrı bir yapılandırma dosyası oluşturulabilir.

### systemd-boot Yönetim Komutları

`bootctl`, systemd-boot kurulumunu ve önyükleme girdilerini yönetir [15]. Kurulum durumunu kontrol etmek için:

```bash
bootctl status
```

Önyükleme girdilerini görüntülemek için:

```bash
bootctl list
```

systemd-boot sürümünü görüntülemek için:

```bash
bootctl --version
```

Önyükleme menüsünün bir sonraki başlangıçta gösterilmesini sağlamak için:

```bash
sudo bootctl set-oneshot @menu
```

Önyükleme girdilerinin yapılandırılması ve yönetimi için EFI System Partition içerisindeki ilgili dosyalar düzenlenebilir.

**Önemli:** systemd-boot kullanıldığında çekirdek ve initramfs dosyalarının firmware tarafından erişilebilir bir konumda bulunması gerekir. Bu nedenle dağıtımın çekirdek güncelleme mekanizmasının ESP üzerindeki dosyaları da güncel tuttuğundan emin olunmalıdır.

## 3. EFISTUB (EFI Boot Stub)

EFISTUB (EFI Boot Stub), Linux çekirdeğinin UEFI firmware tarafından doğrudan bir EFI uygulaması olarak başlatılabilmesini sağlayan çekirdek özelliğidir ([16], [17]).
Normal bir önyükleme sürecinde UEFI önce GRUB veya systemd-boot gibi bir önyükleyiciyi çalıştırır. Bu önyükleyici Linux çekirdeğini belleğe yükler ve gerekli başlangıç parametrelerini iletir.

EFISTUB kullanıldığında ise Linux çekirdeği, UEFI firmware tarafından doğrudan çalıştırılabilecek bir EFI uygulaması olarak sunulur.

Bu sayede GRUB veya systemd-boot gibi ayrı bir önyükleyici kullanmadan Linux çekirdeği başlatılabilir.

Ancak EFISTUB tek başına gelişmiş bir önyükleme yöneticisi değildir. Çoklu işletim sistemi menüsü, otomatik çekirdek keşfi veya kapsamlı yapılandırma yönetimi gibi özellikleri bulunmaz. Bu işlemler UEFI firmware'in sunduğu olanaklara veya harici araçlara bağlıdır.

### Çalışma Mantığı

EFISTUB destekli bir Linux çekirdeği, UEFI firmware tarafından EFI uygulaması olarak algılanır.

Önyükleme sırasında:

1. Linux çekirdeği EFI uygulaması olarak UEFI firmware'e sunulur.
2. Firmware, çekirdek imajını çalıştırır.
3. Çekirdeğe başlangıç parametreleri iletilir.
4. Initramfs belirtilmişse çekirdek tarafından yüklenir.
5. Linux çekirdeği normal başlangıç sürecine devam eder.

EFISTUB desteği Linux çekirdeğinin derleme yapılandırmasına bağlıdır. x86 sistemlerde ilgili yapılandırma seçeneği genellikle `CONFIG_EFI_STUB` olarak adlandırılır.

### Kurulum

EFISTUB kullanabilmek için öncelikle çekirdeğin UEFI tarafından erişilebilir bir EFI System Partition üzerinde bulunması gerekir.

Bazı sistemlerde çekirdek zaten ESP üzerinde tutulabilir. Böyle bir durumda ayrıca kopyalama yapılmasına gerek yoktur.

Örnek olarak çekirdek ve initramfs dosyalarını ESP üzerine kopyalayalım:

```bash
sudo cp /boot/vmlinuz-6.12.113+deb13-amd64 /boot/efi/vmlinuz-linux
sudo cp /boot/initrd.img-6.12.113+deb13-amd64 /boot/efi/initramfs-linux.img
```

Burada:

- `vmlinuz-linux`: EFISTUB üzerinden başlatılacak Linux çekirdeğidir.
- `initramfs-linux.img`: Çekirdeğin başlangıç sırasında kullanacağı initramfs imajıdır.

EFI System Partition'ın yeterli boş alana sahip olması gerekir.

### UEFI Önyükleme Girdisi Oluşturma

EFISTUB ile çekirdeği doğrudan başlatabilmek için UEFI NVRAM üzerinde yeni bir önyükleme girdisi oluşturulabilir.

Bu işlem için `efibootmgr` aracı kullanılır.

Öncelikle ESP'nin hangi disk ve bölüm üzerinde bulunduğu kontrol edilir:

```bash
lsblk -f
```

Ardından örnek bir önyükleme girdisi oluşturulur:

```bash
sudo efibootmgr --create \
    --disk /dev/sda \
    --part 1 \
    --label "Linux EFISTUB" \
    --loader '\vmlinuz-linux' \
    --unicode 'root=UUID=6295c001-c4d7-4e07-acd9-7e6806a8594c ro initrd=\initramfs-linux.img quiet splash'
```

Burada:

- `--disk`: EFI System Partition'ın bulunduğu fiziksel diski belirtir.
- `--part`: EFI System Partition'ın bölüm numarasını belirtir.
- `--label`: Firmware önyükleme menüsünde görüntülenecek adı belirler.
- `--loader`: EFI bölümündeki çekirdek dosyasının yolunu belirtir.
- `--unicode`: Çekirdeğe iletilecek başlangıç parametrelerini tanımlar.

UEFI aygıt yollarında dosya sistemi yolları ters eğik çizgi (`\`) kullanılarak belirtilir. Bu nedenle EFISTUB yapılandırmasında initramfs dosyasının yolu da bu biçimde yazılır.

Oluşturulan önyükleme girdilerini kontrol etmek için:

```bash
sudo efibootmgr -v
```

**Önemli:** Yukarıdaki komut örneğinde `/dev/sda`, bölüm numarası ve UUID değerleri örnektir. Gerçek sistemin disk yapısına göre değiştirilmelidir.

### EFISTUB Kullanımında Dikkat Edilmesi Gerekenler

EFISTUB kullanırken aşağıdaki konulara dikkat edilmelidir:

- Çekirdek imajı UEFI firmware tarafından erişilebilir bir dosya sisteminde bulunmalıdır.
- Initramfs kullanılıyorsa dosyanın konumu ve adı doğru belirtilmelidir.
- Çekirdek parametreleri doğru yapılandırılmalıdır.
- Çekirdek güncellendiğinde ESP üzerindeki çekirdek dosyasının da güncellenmesi gerekir.
- Initramfs yeniden oluşturulduğunda ESP üzerindeki kopyanın da güncellenmesi gerekir.
- UEFI NVRAM girdisinin geçerliliği korunmalıdır.

Bu işlemler otomatikleştirilmediğinde her çekirdek güncellemesinden sonra ilgili dosyaların yeniden kopyalanması gerekebilir.

## 4. systemd-boot, GRUB ve EFISTUB Karşılaştırması

Bu üç çözüm aynı seviyede ve aynı işlevlerle çalışmaz.

GRUB ve systemd-boot, önyükleme menüsü ve işletim sistemi başlatma yönetimi sağlayan önyükleyicilerdir. EFISTUB ise Linux çekirdeğinin doğrudan UEFI tarafından çalıştırılabilmesini sağlayan bir özelliktir.

| Özellik | GRUB2 | systemd-boot | EFISTUB |
|---|---|---|---|
| BIOS desteği | Var | Yok | Yok |
| UEFI desteği | Var | Var | Var |
| Önyükleme menüsü | Var | Var | Firmware'e bağlı |
| Çoklu işletim sistemi desteği | Gelişmiş | EFI girdileri üzerinden | Firmware'e bağlı |
| Modüler yapı | Var | Sınırlı | Yok |
| Yapılandırma | grub.cfg | loader.conf ve entry dosyaları | UEFI NVRAM girdileri |
| Initramfs desteği | Var | Var | Var |
| Dosya sistemi desteği | Geniş | UEFI tarafından erişilebilen dosya sistemleri | UEFI tarafından erişilebilen dosya sistemleri |
| Disk şifreleme yönetimi | Modüllerle mümkün | Doğrudan sunmaz | Doğrudan sunmaz |
| Karmaşık önyükleme senaryoları | Çok uygun | Daha sınırlı | Harici yönetim gerekebilir |

## 5. Önyükleyici Seçerken Dikkat Edilmesi Gerekenler

Linux sistemlerde önyükleyici seçimi yapılırken sistemin donanımı, firmware türü, disk yapılandırması ve kullanım amacı dikkate alınmalıdır.

**GRUB tercih edilebilecek durumlar:**

- BIOS ve UEFI sistemlerin birlikte desteklenmesi gerekiyorsa.
- Birden fazla işletim sistemi kullanılıyorsa.
- Karmaşık disk ve dosya sistemi yapılandırmaları bulunuyorsa.
- Gelişmiş kurtarma ve önyükleme seçeneklerine ihtiyaç duyuluyorsa.

**systemd-boot tercih edilebilecek durumlar:**

- Sistem yalnızca UEFI modunda çalışıyorsa.
- Basit ve kolay yönetilebilir bir önyükleme yapısı isteniyorsa.
- Çekirdek ve initramfs dosyaları ESP üzerinden erişilebilir durumdaysa.
- systemd tabanlı sistemlerde sade bir önyükleme çözümü tercih ediliyorsa.

**EFISTUB tercih edilebilecek durumlar:**

- Harici bir önyükleyici kullanmadan Linux çekirdeğinin doğrudan başlatılması isteniyorsa.
- Basit bir UEFI önyükleme yapısı hedefleniyorsa.
- Çekirdek parametreleri ve NVRAM girdileri doğrudan yönetilebiliyorsa.

---

*Not: Önyükleyici kurulumu ve yapılandırması dağıtıma, firmware mimarisine ve disk düzenine göre farklılık gösterebilir. Komut örnekleri uygulanmadan önce sistemin gerçek disk ve bölüm bilgileri kontrol edilmelidir.*

Önyükleyici, seçilen çekirdek imajını ve başlangıç parametrelerini yükleyip kontrolü çekirdeğe devreder. Sıradaki bölümde çekirdeğin bu kontrolü aldıktan sonra işlemciyi, belleği ve temel alt sistemleri nasıl hazırladığını izleyeceğiz.
