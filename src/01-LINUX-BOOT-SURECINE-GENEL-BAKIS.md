# Linux Boot Sürecine Genel Bakış

## 1. POST ve Donanım Kontrolü:
Bilgisayarın tuşuna basıldığında bilgisayar ilk olarak donanım testi (POST) işlemini gerçekleştirir.

## 2. Anakart Yazılımı (BIOS/UEFI):
Eğer test başarılıysa anakart yazılımı (eski sistemlerde BIOS, modern sistemlerde UEFI) devreye girerek diski tarar ve önyükleyiciyi bulur.

## 3. Önyükleyici (Bootloader):
Önyükleyici (örneğin GRUB) başlatılır. Kullanıcıya kernel seçeneklerini sunar. Ardından sistemin bulunduğu disk içerisinden sıkıştırılmış durumdaki Linux çekirdeğini (vmlinuz) ve initramfs dosyasını RAM'e çekip sistemi başlatır.

## 4. Çekirdek (Kernel) Başlangıcı:
Linux çekirdeği RAM'de kendi kendini açar, temel donanımları tanır ve initramfs içerisindeki mini sistemi (initrd) tetikler.

## 5. initramfs ve Asıl Diskin Bağlanması:
Çekirdek, initramfs içerisindeki bu mini sistemi kullanarak asıl başlatılacak sistemin bulunduğu diski bağlama, varsa parola sorma ve şifrelemeyi çözme (LUX/DM-Crypt) işlemlerini gerçekleştirir.

## 6. Kök Dizine Geçiş (Pivot Root):
İşlem tamamlandığında linux çekirdeği geçici initramfs dosya sistemini RAM'den temizler ve pivot_root yaparak çalıştırılacak olan asıl diske (kök dizine - /) geçiş yapar.

## 7. İnit Sisteminin Devralması:
Bu noktadan sonra sistemin içerisindeki ilk süreç olan PID 1 (init) başlatılmış olur. İnit sistemi (systemd, openrc, sysvinit vb.) sistemdeki servisleri (ağ, günlük tutma, ses vb.) olması gereken sırayla ve gereken parametrelerle başlatır.

## 8. Kullanıcı Ekranı (GUI/TUI):
Tüm gereken servisler başladıktan sonra, grafiksel bir sistemse görüntü yöneticisi (Display Manager) veya terminal giriş ekranı (Getty) çağrılır ve karşımıza giriş ekranı gelir. Giriş yapıldığında sistem tamamen başlatılmış ve kullanıma hazır hale gelir.