# Linux Çekirdeği (Kernel)

Önyükleyici (Bootloader), çekirdek imajını (`vmlinuz`) ve geçici kök dosya sistemini (`initramfs`) belleğe yükleyip kontrolü devrettikten sonra Linux işletim sisteminin kalbi olan **Kernel** devreye girer.
Bu bölümde, sıkıştırılmış bir imajın nasıl kendi kendini açtığını, donanım ilklendirmelerini ve sistemin kullanıcı alanına (user space) nasıl hazırlandığını derinlemesine inceleyeceğiz.

## Vmlinuz Anatomisi

Modern Linux dağıtımlarında çekirdek, diskte genellikle `/boot/vmlinuz-<versiyon>` adıyla saklanır.
Buradaki **"vmli"** (Virtual Memory Linux) sanal bellek desteğini, sondaki **"z"** ise imajın sıkıştırılmış (compressed) olduğunu ifade eder.

`vmlinuz` aslında kendi kendini açabilen (self-extracting) iki ana bölümden oluşan bir **bzImage** (Big ZImage) yapısıdır:


| bzImage Bileşenleri | Görevi / Özelliği |
|---------------------|-------------------|
|Setup Code (Gerçek Mod) | Bilgisayar ilk açıldığında donanımı hazırlar ve işlemciyi korumalı moda geçirir.|
|Stub / Decompressor Code | Sıkıştırılmış asıl çekirdek kodunu açarak belleğe yükler.|
|Sıkıştırılmış Çekirdek (vmlinux.bin.gz/xz/lz4) | İşletim sisteminin tüm ana işlevlerini barındıran sıkıştırılmış asıl gövdedir.|


1. **Setup & Decompressor Başlığı:** Çekirdeğin en başında yer alan, işlemci modunu değiştiren ve sıkıştırılmış asıl çekirdeği açan küçük bir kod blokudur (genellikle `gzip`, `xz`, `lz4` veya `zstd` algoritmasıyla sıkıştırılır).
2. **vmlinux (Asıl Çekirdek):** Sıkıştırılmamış, çalıştırılabilir ELF formatındaki gerçek Linux çekirdeğidir.

## Gerçek Moddan (Real mode) Korumalı Moda (Protected mode) Geçiş

x86_64 mimarisine sahip modern bir işlemci bile boot anında geriye dönük uyumluluk adına **Real Mode (Gerçek Mod)** ile başlar.
Çekirdeğin ilk görevi işlemciyi modern modlara taşımaktır:

1. **Real Mode (16-bit):** Bellek erişimi 1 MB ile sınırlıdır. Önyükleyiciden alınan parametreler okunur.
2. **Protected Mode (32-bit):** `head_32.S` veya ilgili assembly kodları çalıştırılarak **GDT (Global Descriptor Table)** ve **IDT (Interrupt Descriptor Table)** geçici olarak kurulur.İşlemci artık 4 GB belleğe erişebilir.
3. **Long Mode (64-bit):** Sayfalama (Paging) aktif edilir ve işlemci tam 64-bit moduna (`head_64.S`) geçirilir.

İşlemci 64-bit Long Mode'a geçtikten sonra, sıkıştırma açıcı fonksiyon (`decompress_kernel`) tetiklenir ve asıl çekirdek (`vmlinux`) belleğin güvenli bir bölgesine (genellikle `0x100000` - 1MB adresinin üzerine) açılır.
Kontrol, çekirdeğin mimariden bağımsız ilk C fonksiyonu olan `start_kernel()` mimarisine devredilir.

## start_kernel() ve Çekirdek Subsistemleri

`init/main.c` dosyasında yer alan **`start_kernel()`** fonksiyonu, Linux çekirdeğinin ana yönetim merkezidir.
Bu aşamada henüz hiçbir süreç (process) veya kullanıcı arayüzü yoktur.
Sırasıyla şu alt sistemler ilklendirilir:

| Fonksiyon / Bileşen | Görevi |
| :--- | :--- |
| `setup_arch()` | Mimariye özgü (x86, ARM vb.) donanım tanımlamalarını ve komut satırı parametrelerini (`boot_command_line`) işler. |
| `mm_init()` | Bellek yönetim sistemini (Memory Management) kurar. |
| `sched_init()` | Süreç zamanlayıcıyı (Scheduler) başlatır. Görevler arası geçiş yeteneği kazanılır. |
| `trap_init()` | İşlemci donanım kesmelerini (Hatalar, istisnalar) yakalayacak tabloları kurar. |
| `init_IRQ()` | Donanım aygıtlarından gelecek kesme isteklerini (Interrupt Requests) yapılandırır. |
| `vfs_caches_init()`| Sanal Dosya Sistemi (VFS) önbelleklerini oluşturur. |

## Çekirdek Parametreleri (Kernel Cmdline)

Önyükleyicinin (GRUB) çekirdeğe gönderdiği parametreler, çekirdeğin davranışını doğrudan belirler.
Bunlar `/proc/cmdline` dosyasından da okunabilir:

* `ro`: Kök dosya sistemini ilk olarak salt okunur (read-only) bağla.
* `root=UUID=...`: Sistemin açılacağı asıl kök diskin kimliği.
* `quiet`: Açılış esnasındaki yoğun log akışını gizle.
* `splash`: Grafiksel açılış ekranını (Plymouth gibi) aktif et.
* `init=...`: Varsayılan PID 1 sürecini değiştir (Örn: `init=/bin/bash` ile kurtarma modu).

## PID 0 (Idle Process) ve PID 1

1. PID 0 (Boşta Kalma Süreci): Bilgisayar ilk açıldığında start_kernel() adlı ana bir kod bloğu çalışır.
Bu kodun işi bittiğinde, arka planda PID 0 (swapper/idle) adında bir sürece dönüşür.
Görevi bilgisayarda yapacak hiçbir iş kalmadığında işlemciyi uyku moduna alıp güç tasarrufu sağlamaktır.

2. PID 1 (İlk Kullanıcı Süreci): Hazırlıklar bitince kernel_init görevi, bilgisayarın asıl kontrolünü kullanıcıya devrederek PID 1 (init) sürecini başlatır.
PID 1, bilgisayar açık olduğu sürece çalışan tüm diğer programların ve uygulamaların "atası" (ilk başlatanı) olur.

## Hata Ayıklama

Çekirdeğin yüklenme ve ilklendirme aşamasındaki tüm loglar bellek içi bir halka arabellekte (ring buffer) tutulur.

* **dmesg:** Çekirdek log halka arabelleğini ekrana basar. Açılış hatalarını yakalamak için en kritik komuttur.
  ```bash
  dmesg | grep -i -E 'memory|cpu|acpi'
  ```
* **/proc/cpuinfo ve /proc/meminfo:** Çekirdeğin donanımdan topladığı ve maplediği işlemci ile bellek detayları.


