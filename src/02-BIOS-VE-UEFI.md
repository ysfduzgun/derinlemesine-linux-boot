# BIOS ve UEFI Nedir? (Önyükleme Öncesi Aşama)

Bilgisayarın güç tuşuna basıldıktan sonra, işletim sistemi (Linux Çekirdeği) henüz devralmadan önce donanımı ayağa kaldıran ve önyükleyiciyi (Bootloader) bulan iki temel anakart yazılım teknolojisi vardır: **BIOS** ve **UEFI**.

## 1. BIOS (Basic Input/Output System) ve MBR
1970'lerden beri kullanılan geleneksel ve eski (legacy) bir yazılımdır.

### Çalışma Mantığı:
1. **POST (Power-On Self Test):** Donanımları test eder.
2. **Boot Sıralaması:** BIOS ayarlarında belirtilen disk sırasına göre ilk diski okur.
3. **MBR (Master Boot Record):** Diskin en başındaki ilk **512 baytlık** özel sektöre (MBR) bakar.
4. **Tetikleme:** MBR içerisindeki önyükleyici kodunu (GRUB Stage 1 gibi) RAM'e yükler ve kontrolü ona devreder.

### Limitleri:
* Sadece **2 TB**'a kadar olan disk boyutlarını destekler.
* Bir diskte en fazla **4 adet birincil (primary) bölüm** oluşturulabilir.
* 16-bit işlemci modunda (real mode) çalışır ve çok yavaştır.

## 2. UEFI (Unified Extensible Firmware Interface) ve GPT
Modern bilgisayarlarda BIOS'un yerini alan, daha gelişmiş, esnek ve güvenli bir arayüz standartıdır.

### Çalışma Mantığı:
1. **POST (Power-On Self Test):** Donanımları çok daha hızlı bir şekilde test eder.
2. **GPT (GUID Partition Table):** UEFI, eski MBR yerine modern GPT disk yapısını kullanır. GPT, disk bölümlerini benzersiz kimliklerle (GUID) tanımlar.
3. **ESP (EFI System Partition):** UEFI, disk sektörlerini doğrudan okumak yerine diskin içindeki **FAT32** formatındaki özel bir bölümü (**ESP**) okur.
4. **Tetikleme:** ESP içerisindeki `.efi` uzantılı önyükleyici dosyasını (örneğin: `/EFI/BOOT/BOOTX64.EFI` veya Linux için `/EFI/pardus/grubx64.efi`) bulur ve doğrudan çalıştırır.

### Avantajları:
* **9.4 Zettabayt** boyutundaki devasa diskleri destekler.
* **128'e kadar**  birincil disk bölümü oluşturulabilir.
* 32-bit veya 64-bit modunda çalışır; sürücüleri kendi içinde yükleyebildiği için fare desteği, grafik arayüz ve internete bağlanma gibi yetenekleri vardır.

## BIOS ve UEFI Karşılaştırma Tablosu

| Özellik | Geleneksel BIOS | Modern UEFI |
| :--- | :--- | :--- |
| **Disk Bölüm Tablosu** | MBR (Master Boot Record) | GPT (GUID Partition Table) |
| **Maksimum Disk Boyutu**| 2 Terabayt (TB) | 9.4 Zettabayt (ZB) |
| **Maksimum Bölüm Sayısı**| 4 Birincil Bölüm | 128 Birincil Bölüm |
| **Çalışma Modu** | 16-bit (Yavaş, Metin Tabanlı) | 32/64-bit (Hızlı, Grafik Arayüzlü)|
| **Önyükleyici Konumu** | Diskin ilk 512 baytlık sektörü | ESP (FAT32 Bölümü içindeki `.efi` dosyası) |
| **Güvenlik (Secure Boot)**| Yok | Var |

## Linux Üzerinde Sistem Türünü Kontrol Etme
Mevcut çalışan Linux sisteminizin BIOS mu yoksa UEFI mi kullandığını anlamak için terminalde şu komut çalıştırılır:

```bash
[ -d /sys/firmware/efi ] && echo "Sistem: UEFI" || echo "Sistem: BIOS / Geleneksel"
```

Eğer `/sys/firmware/efi` dizini mevcutsa sistem **UEFI** modunda başlatılmıştır.

