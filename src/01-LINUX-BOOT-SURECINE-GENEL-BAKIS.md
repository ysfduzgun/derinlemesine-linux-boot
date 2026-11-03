# Linux boot sürecine genel bakış
Bilgisayarın tuşuna basıldığında bilgisayar ilk olarak donanım testi (POST) işlemini gerçekleştirir.
Eğer test başarılıysa önyükleyici başlatılır.
Önyükleyici sistemin bulunduğu disk içerisinden çekirdeği ve initramfs dosyasını bulup sistemi başlatır.
Linux çekirdeği initramfs içerisindeki mini sistemi kullanarak asıl başlatılacak sistemin bulunduğu diski bağlama, varsa parola sorma ve şifrelemeyi çözme işlemlerini gerçekleştirir.
Son olarak linux çekirdeği initramfs dosya sistemini imha ederek çalıştırılacak olan sisteme geçiş yapar.
Bu noktadan sonra sistemin içerisindeki init başlatılmış olur.
İnit sistemi (systemd, openrc, sysvinit vb) sistemdeki servisleri olması gereken sırayla ve gereken parametrelerle başlatır.
Tüm gereken servisler başladıktan sonra sistem tamamen başlatılmış ve kullanıma hazır hale gelir.
