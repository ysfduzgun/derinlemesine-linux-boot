# Terimler ve Kısaltmalar

| Terim / kısaltma | İngilizce açılımı | Türkçe açıklama |
|---|---|---|
| BIOS | Basic Input/Output System | Eski nesil sistemlerde donanımı başlatan ve önyükleme sürecini başlatan firmware arayüzü. |
| Boot / Booting | Boot / Booting | Bilgisayarın açılıp işletim sisteminin çalışır duruma gelmesi süreci; Türkçede önyükleme veya açılış denir. |
| Bootloader | Boot Loader | Çekirdeği ve gerekli başlangıç dosyalarını yükleyerek kontrolü işletim sistemine devreden önyükleyici yazılım. |
| bzImage | Big ZImage | x86 sistemlerde kullanılan, önyükleme kodu ve sıkıştırılmış çekirdek içeren çekirdek imajı biçimi. Adındaki `bz`, bzip2 ile sıkıştırıldığı anlamına gelmez. |
| CPIO | Copy In and Out | Dosya ve dizinleri arşivlemek için kullanılan biçim; initramfs içinde yaygın olarak kullanılır. |
| CPU | Central Processing Unit | Merkezi işlem birimi; komutları çalıştıran işlemci. |
| db / dbx | Signature Database / Forbidden Signature Database | UEFI Secure Boot’ta izin verilen ve yasaklanan imzaları içeren veritabanları. |
| Decompressor | Decompressor | Sıkıştırılmış veriyi açan kod veya yazılım bileşeni. Çekirdek imajındaki açıcı kod, çekirdeği belleğe açar. |
| Daemon | Daemon | Genellikle arka planda çalışan ve sistem ya da uygulama hizmeti sunan süreç. |
| EFI | Extensible Firmware Interface | UEFI sistemlerde firmware ile önyükleme uygulamaları arasındaki arayüz ve uygulama biçimi. |
| ESP | EFI System Partition | UEFI önyükleme uygulamalarını ve ilgili dosyaları barındıran özel disk bölümü. |
| EFISTUB | EFI Boot Stub | Linux çekirdeğinin UEFI firmware tarafından doğrudan EFI uygulaması olarak başlatılmasını sağlayan özellik. |
| ELF | Executable and Linkable Format | Linux ve diğer Unix benzeri sistemlerde yürütülebilir dosyalar, nesne dosyaları ve kütüphaneler için kullanılan biçim. |
| Firmware | Firmware | Donanım üzerinde çalışan, aygıtı başlatan ve temel işlevlerini sağlayan yazılım. BIOS ve UEFI firmware örnekleridir. |
| GPT | GUID Partition Table | Disk bölümlerini tanımlamak için kullanılan modern bölümleme tablosu biçimi. |
| GRUB | GRand Unified Bootloader | Linux ve diğer işletim sistemlerini başlatabilen, yaygın kullanılan önyükleyici. |
| GUID | Globally Unique Identifier | Bir nesneyi veya disk bölümünü tanımlamak için kullanılan küresel ölçekte benzersiz kimlik değeri. |
| GDT | Global Descriptor Table | x86 işlemcilerde bellek segmentleri ve çalışma kipleriyle ilgili tanımları tutan tablo. |
| IDT | Interrupt Descriptor Table | x86 işlemcilerde kesme ve istisnaların hangi işleyicilere yönlendirileceğini belirleyen tablo. |
| Init | Initialization / init | Kullanıcı alanındaki başlangıç süreci ve sistem hizmetlerini başlatıp yöneten program için kullanılan ad. Linux'ta geleneksel olarak PID 1 sürecidir. |
| Initramfs | Initial RAM Filesystem | Gerçek kök dosya sistemine geçmeden önce çekirdeğin bellekte kullandığı geçici başlangıç dosya sistemi ve kullanıcı alanı ortamı. |
| Initrd | Initial RAM Disk | Başlangıçta belleğe yüklenen disk imajı yaklaşımı. Initramfs ile ilişkili olsa da aynı mekanizma değildir. |
| IRQ | Interrupt Request | Donanım aygıtının işlemciden dikkat istemek için gönderdiği kesme isteği. |
| KEK | Key Exchange Key | UEFI Secure Boot’ta imza veritabanlarını güncellemeye yetki veren anahtar. |
| Kernel | Kernel | İşletim sisteminin donanım, bellek, süreç ve aygıt kaynaklarını yöneten çekirdek bileşeni. |
| Kernel space | Kernel Space | Çekirdek kodunun çalıştığı ve çekirdeğe ayrılmış bellek alanı. |
| Long mode | Long Mode | x86-64 işlemcilerin 64 bit işletim ve adresleme özelliklerini sağlayan çalışma kipi. |
| MBR | Master Boot Record | Geleneksel disk bölümleme biçiminde diskin ilk sektöründe bulunan önyükleme kodu ve bölüm tablosu yapısı. |
| Microcode | Microcode | İşlemci içindeki bazı komutların ve donanım davranışlarının uygulanmasını yöneten düşük seviyeli işlemci kodu. |
| NVRAM | Non-Volatile Random-Access Memory | Güç kapalıyken de içeriğini koruyan bellek. UEFI önyükleme girdileri burada saklanabilir. |
| OpenRC | OpenRC | Linux ve Unix benzeri sistemlerde hizmetleri ve açılış aşamalarını yöneten init sistemi. |
| PID | Process Identifier | Bir süreci tanımlamak için işletim sistemi tarafından verilen süreç numarası. |
| POST | Power-On Self-Test | Bilgisayar açılırken firmware tarafından yapılan temel donanım denetimi. |
| PK | Platform Key | UEFI Secure Boot’ta platformun güven ilişkisini ve anahtar hiyerarşisini belirleyen anahtar. |
| Protected mode | Protected Mode | x86 işlemcilerin korumalı bellek ve gelişmiş işlemci özellikleri sağlayan 32 bit çalışma kipi. |
| PTY | Pseudo Terminal | Bir programın terminal aygıtı gibi kullanabildiği yazılım tabanlı terminal çifti. Uzak oturumlarda ve terminal emülatörlerinde kullanılır. |
| RAM | Random-Access Memory | Çalışan programların ve verilerin geçici olarak tutulduğu ana bellek. |
| Real mode | Real Mode | x86 işlemcilerin başlangıçta desteklediği, eski yazılımlarla uyumluluk sağlayan 16 bit çalışma kipi. |
| Root filesystem / rootfs | Root Filesystem | Linux sisteminin `/` olarak bağlanan kök dosya sistemi. Initramfs aşamasında kullanılan geçici rootfs ile gerçek kök dosya sistemi farklıdır. |
| Runlevel | Runlevel | SysVinit ve OpenRC gibi init sistemlerinde servis kümesini ve sistemin çalışma durumunu belirten seviye. |
| Scheduler | Scheduler | İşlemci zamanını çalışmaya hazır süreçler arasında paylaştıran çekirdek bileşeni; Türkçede zamanlayıcı denir. |
| Secure Boot | Secure Boot | UEFI'nin, önyükleme zincirindeki yazılımların imzalarını doğrulayarak başlatılmasına izin veren güvenlik özelliği. |
| Shell | Shell | Kullanıcıdan komut alıp bunları çalıştıran komut yorumlayıcısı; Türkçede kabuk denir. |
| Socket activation | Socket Activation | Bir hizmetin, kendisi için tanımlanmış ağ veya IPC soketine bağlantı geldiğinde başlatılması yöntemi. systemd tarafından desteklenir. |
| SSH | Secure Shell | Uzak bir bilgisayara şifreli bağlantı kurup komut çalıştırmayı sağlayan protokol ve araç ailesi. |
| SysVinit | System V init | Unix System V yaklaşımından gelen, runlevel ve servis betikleri kullanan init sistemi. |
| systemd | systemd | Linux sistemlerinde init süreci olmanın yanı sıra hizmetleri ve sistem kaynaklarını yöneten yazılım paketi. Adı bir kısaltma değildir. |
| Target | Target | systemd'de sistemin belirli bir çalışma durumunu veya ilişkili birim grubunu temsil eden birim türü. |
| TTY | Teletypewriter | Metin tabanlı terminal aygıtı veya arayüzü için kullanılan ad; sanal konsollar da TTY olarak sunulur. |
| UEFI | Unified Extensible Firmware Interface | Modern bilgisayarlarda donanımı başlatan ve EFI uygulamalarını çalıştıran firmware arayüzü. |
| Unit | Unit | systemd'nin hizmet, bağlama noktası, aygıt veya hedef gibi kaynakları tanımlayıp yönetmek için kullandığı yapılandırma birimi. |
| User space | User Space | Çekirdek dışında çalışan uygulama ve hizmetlerin bulunduğu kullanıcı alanı. |
| UUID | Universally Unique Identifier | Bir dosya sistemini veya başka bir kaynağı tanımlamak için kullanılan benzersiz kimlik. Disk bölümlerini aygıt adından bağımsız tanımlamakta kullanılır. |
| VFS | Virtual File System | Farklı dosya sistemlerine ortak bir arayüz üzerinden erişim sağlayan sanal dosya sistemi katmanı. |
| vmlinuz | — | Önyüklemeye uygun, genellikle sıkıştırılmış Linux çekirdek imajının yaygın dosya adı. Dosya adının tarihsel kökeni, biçimin içeriğini tek başına açıklamaz. |
| vmlinux | — | Genellikle ELF biçimindeki, sıkıştırılmamış Linux çekirdeği imajı için kullanılan ad. |
| Workqueue | Workqueue | Çekirdeğin bazı işleri daha sonra süreç bağlamında çalıştırmak üzere kuyruğa koymasını sağlayan altyapı. |
